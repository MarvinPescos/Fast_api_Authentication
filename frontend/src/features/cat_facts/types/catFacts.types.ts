export interface CatFactSubscription {
  id: number;
  user_id: number;
  is_active: boolean;
  preferred_time: string;
  timezone: string;
  last_sent_at: string | null;
  total_sent: number;
  created_at: string;
  updated_at: string | null;
}

export interface SubscriptionStatus {
  subscribed: boolean;
  subscription: CatFactSubscription | null;
  message: string;
}

export interface CatFact {
  fact: string;
  source: string;
  length: number;
  fetched_at: string;
}

export interface SubscriptionFormData {
  preferred_time?: string;
  timezone?: string;
}
