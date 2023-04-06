/** The format of movie data received from the Webservices api */
export interface Movie {
    /** The movie title */
    title: string;
    /** The movie TMDB id */
    id: number;
    /** The movie runtime */
    runtime?: number;
    /** The movie TMDB genre ids */
    genre_ids?: Array<number>;
    /** The movie Webservices API like status */
    liked: boolean;
}