import { z } from "zod";

export const BuildingSchema = z.object({
  id: z.number(),
  building_name: z.string().min(3).max(50),
  architectural_style: z.string().optional(),
});

export const RatingSchema = z.object({
  id: z.number(),
  building_id: z.number(),
  aesthetic_rating: z.number().min(1).max(10),
  functionality_rating: z.number().min(1).max(10),
  photo_worthiness: z.number().min(1).max(10),
  instagram_potential: z.number().min(1).max(10),
  weirdness_factor: z.number().min(1).max(10),
});

export const CreateRatingSchema = z.object({
  building_id: z.number(),
  aesthetic_rating: z.number().min(1).max(10),
  functionality_rating: z.number().min(1).max(10),
  photo_worthiness: z.number().min(1).max(10),
  instagram_potential: z.number().min(1).max(10),
  weirdness_factor: z.number().min(1).max(10),
});

export type BuildingType = z.infer<typeof BuildingSchema>;
export type RatingType = z.infer<typeof RatingSchema>;
export type CreateRatingType = z.infer<typeof CreateRatingSchema>;
