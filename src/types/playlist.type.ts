import { UserType } from "./user.type";
import { VideoType } from "./video.type";

export interface PlaylistType {
  id: string;
  name: string;
  description: string;
  author: UserType;
  videos: VideoType[];
  thumbnail: string;
  public: boolean;
}
