import { PlaylistType } from "./playlist.type";
import { VideoType } from "./video.type";

export interface UserType {
    id: string;
    name: string;
    username: string;
    bio: string;
    pub_blogs: VideoType[];
    pub_playlists: PlaylistType[];
    dp: string;
    shapka: string;
    no_of_following: number;
    no_of_followers: number;
    no_of_blogs: number;
    main_name: string;
    main_link: string;
    second_name: string;
    second_link: string;
    third_name: string;
    third_link: string;
    fourth_name: string;
    fourth_link: string;
    fifth_name: string;
    fifth_link: string;
}