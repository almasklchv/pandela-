import { UserType } from "./user.type";

export interface VideoType {
  author: {
    id: string;
    name: string;
    username: string;
    dp: string;
    no_of_followers: string;
  };
  id: string;
  title: string;
  description: string;
  video: string;
  thumbnail: string;
  is_published: boolean;
  likes: UserType[];
  saves: UserType[];
  no_of_views: number;
  views: number;
  no_of_likes: number;
  no_of_saves: number;
  tags: [];
  playlist_setting: string;
}
