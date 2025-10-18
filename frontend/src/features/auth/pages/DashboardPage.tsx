import { useAuthStore } from "../store/authStore";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

interface Activity {
  id: string;
  title: string;
  description: string;
  path: string;
  category: string;
}

export function DashboardPage() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [activeNav, setActiveNav] = useState<string>("dashboard");
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  // Helper function to get user display name
  const getUserDisplayName = () => {
    if (!user) return "User";
    return (
      user.full_name || user.username || user.email?.split("@")[0] || "User"
    );
  };

  // Helper function to get user initials
  const getUserInitials = () => {
    if (!user) return "U";
    const displayName = getUserDisplayName();
    const nameParts = displayName.split(" ");
    if (nameParts.length >= 2) {
      return (nameParts[0][0] + nameParts[1][0]).toUpperCase();
    }
    return displayName[0]?.toUpperCase() || "U";
  };

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const handleActivityClick = (path: string) => {
    navigate(path);
  };

  const handleNavClick = (navItem: string) => {
    setActiveNav(navItem);
    // Navigate to the selected page
    if (navItem === "home") {
      navigate("/home");
    } else if (navItem === "profile") {
      navigate("/profile");
    }
  };

  // Fetch user data and activities
  useEffect(() => {
    const fetchActivities = async () => {
      try {
        // TODO: Replace with actual API call when backend endpoints are ready
        // For now, using static data but structured properly
        const mockActivities: Activity[] = [
          {
            id: "cat-facts",
            title: "Cat Facts",
            description: "Subscribe to daily cat facts delivered to your email",
            path: "/activities/cat-facts",
            category: "Entertainment",
          },
          {
            id: "trivia",
            title: "Trivia Game",
            description: "Test your knowledge with random trivia questions",
            path: "/activities/trivia",
            category: "Games",
          },
          {
            id: "ciphers",
            title: "Text Ciphers",
            description:
              "Encode and decode text using various cipher algorithms",
            path: "/activities/ciphers",
            category: "Tools",
          },
          {
            id: "qr-generator",
            title: "QR Generator",
            description: "Generate QR codes from any text or URL",
            path: "/activities/qr-generator",
            category: "Tools",
          },
          {
            id: "building-rater",
            title: "Campus Building Rater",
            description: "Rate and review campus buildings on various criteria",
            path: "/activities/campus-building-rater",
            category: "Social",
          },
          {
            id: "joke-cipher-qr",
            title: "Joke Cipher QR",
            description: "Fetch jokes, apply ciphers, and generate QR codes",
            path: "/activities/joke-cipher-qr",
            category: "Entertainment",
          },
        ];

        setActivities(mockActivities);
      } catch (error) {
        // Silently handle error - activities are not critical
      }
    };

    const initializeData = async () => {
      await fetchActivities();
      setLoading(false);
    };

    initializeData();
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <div className="p-6 border-b border-gray-200">
            <h1 className="text-xl font-bold text-gray-900">Mini-Apps</h1>
            <p className="text-xs text-gray-500 mt-1">Activity Hub</p>
          </div>
          <div className="flex-1 p-4 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
          </div>
        </aside>
        <main className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading activities...</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Left Sidebar Navigation */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        {/* Logo/Brand */}
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-900">Mini-Apps</h1>
          <p className="text-xs text-gray-500 mt-1">Activity Hub</p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          <button
            onClick={() => handleNavClick("dashboard")}
            className={`w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
              activeNav === "dashboard"
                ? "bg-amber-50 text-amber-700"
                : "text-gray-700 hover:bg-gray-100"
            }`}
          >
            <svg
              className="w-5 h-5 mr-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            Dashboard
          </button>

          <button
            onClick={() => handleNavClick("profile")}
            className={`w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
              activeNav === "profile"
                ? "bg-amber-50 text-amber-700"
                : "text-gray-700 hover:bg-gray-100"
            }`}
          >
            <svg
              className="w-5 h-5 mr-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            Profile
          </button>
        </nav>

        {/* User Profile Card in Sidebar */}
        <div className="p-4 border-t border-gray-200">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center">
                <span className="text-amber-700 font-semibold text-sm">
                  {getUserInitials()}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {getUserDisplayName()}
                </p>
                <p className="text-xs text-gray-500 truncate">{user?.email}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="w-full mt-3 px-3 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto">
        {/* Top Header */}
        <header className="bg-white border-b border-gray-200">
          <div className="px-8 py-6">
            <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
            <p className="text-sm text-gray-600 mt-1">
              Welcome back, {getUserDisplayName()}
            </p>
          </div>
        </header>

        {/* Content */}
        <div className="p-8">
          {/* Activities Section */}
          <section>
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Available Activities
              </h2>
              <p className="text-gray-600">
                Explore our collection of interactive tools and features
              </p>
            </div>

            {/* Activities Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activities.map((activity) => (
                <button
                  key={activity.id}
                  onClick={() => handleActivityClick(activity.path)}
                  className="bg-white border border-gray-200 rounded-lg p-6 text-left hover:border-gray-300 hover:shadow-md transition-all group"
                >
                  {/* Category Badge */}
                  <div className="mb-3">
                    <span className="inline-block px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-full">
                      {activity.category}
                    </span>
                  </div>

                  {/* Title */}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-gray-700">
                    {activity.title}
                  </h3>

                  {/* Description */}
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {activity.description}
                  </p>

                  {/* Arrow Icon */}
                  <div className="mt-4 flex items-center text-sm font-medium text-amber-500 group-hover:text-amber-600">
                    <span>Explore</span>
                    <svg
                      className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </div>
                </button>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
