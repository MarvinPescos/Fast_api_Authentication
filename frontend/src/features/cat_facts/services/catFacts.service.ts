import api from "../../../shared/services/api";
import type {
  SubscriptionStatus,
  CatFact,
  SubscriptionFormData,
} from "../types/catFacts.types";

export class CatFactsService {
  async getSubscriptionStatus(): Promise<SubscriptionStatus> {
    try {
      const response = await api.get(
        "/fullstack_authentication/activities/cat-facts/status"
      );
      return response as unknown as SubscriptionStatus;
    } catch (error: any) {
      console.error("Failed to fetch subscription status:", error);
      throw new Error("Failed to fetch subscription status");
    }
  }

  async subscribe(data: SubscriptionFormData = {}): Promise<any> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/cat-facts/subscribe",
        data
      );
      return response as unknown as any;
    } catch (error: any) {
      console.error("Failed to subscribe:", error);

      if (error.response?.status === 409) {
        throw new Error("You're already subscribed to cat facts!");
      }

      throw new Error("Failed to subscribe to cat facts");
    }
  }

  async unsubscribe(): Promise<any> {
    try {
      const response = await api.delete(
        "/fullstack_authentication/activities/cat-facts/unsubscribe"
      );
      return response as unknown as any;
    } catch (error: any) {
      console.error("Failed to unsubscribe:", error);
      throw new Error("Failed to unsubscribe from cat facts");
    }
  }

  async getRandomCatFact(): Promise<CatFact> {
    try {
      const response = await api.get(
        "/fullstack_authentication/activities/cat-facts/random"
      );
      return response as unknown as CatFact;
    } catch (error: any) {
      console.error("Failed to fetch cat fact:", error);
      throw new Error("Failed to fetch cat fact");
    }
  }
}

export const catFactsService = new CatFactsService();
