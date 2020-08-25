import pytumblr
import sys
import logging

logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s Line: %(lineno)d",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger().addHandler(logging.StreamHandler())

from configs import (
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_SECRET,
    OAUTH_TOKEN,
    BLOG_NAME,
    LIMIT,
    TIMESTAMP_FILE,
)


def get_timestamp_from_file(file_name):
    """Read the saved timestamp from file
     Parameters
        ----------
        file_name : str
            Name of the file
        
        Returns
        -------
        int
            Last saved timestamp on file or 0 if no data on file
    """
    timestamp = 0
    with open(file_name, "r") as timestamp_file:
        timestamp_string = timestamp_file.read().strip()
        if timestamp_file:
            if timestamp_string.isdigit():
                if len(timestamp_string) > 10:
                    logging.info("Are you from heaven? Is Tumblr still around?")
                    input("Press Enter to continue or CTRL + C to get back to earth.")

                timestamp = int(timestamp_string)

            else:
                # timestamp not valid, contains non-numeric characters
                logging.error(
                    "Timestamp format not valid. Timestamp should be in UNIX timestamp format."
                )
                logging.info(
                    "For more about UNIX timestamp, please check - https://en.wikipedia.org/wiki/Unix_time"
                )

                sys.exit(1)

    return timestamp


def write_timestamp_to_file(file_name, timestamp):
    """Save last timestamp to file
     Parameters
        ----------
        file_name : str
            Name of the file
        timestamp: int
            Timestamp to save
        
        Returns
        -------
        None
    """
    with open(file_name, "w") as timestamp_file:
        timestamp_file.write(str(timestamp))


def get_likes_list(client, timestamp, limit=50):
    """Get data of 50 likes that were liked after the timstamp from Tumblr API
     Parameters
        ----------
        client : TumblrRestClient object
            Handles the connection with Tumblr API
        timestamp : int
            Data will be fetched of posts that were liked after this timestamp
        limit : int, optional
            Number (maximum) of posts that to be fetched in a batch. 
        
        Returns
        -------
        dict
            A dict containing the liked posts data.
            Or emtpy in case of errors with connection.
    """

    if limit > 50:
        logging.warning(
            f"Provided limit is {limit}. Tumblr defaults limit to 50 for any values over 50."
        )

    try:
        # get the data
        likes_list = client.likes(after=timestamp, limit=50)
        ret_data = likes_list["liked_posts"]
        ret_data.reverse()
        return ret_data

    except Exception as tumblr_api_connection_error:
        logging.error(tumblr_api_connection_error)
        logging.info("Something went wrong with connecting to Tumblr API")

        return {}


def main():
    """Run this thing"""

    timestamp = get_timestamp_from_file(TIMESTAMP_FILE)

    # create tumblr client
    client = pytumblr.TumblrRestClient(
        CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET
    )

    # print(client.info())

    # This is flood bot
    # Tries to post upto 250 posts if available

    for x in range(5):
        if x == 0:
            timestamp = timestamp
        else:
            timestamp = liked_posts[-1]["liked_timestamp"]

        # get the posts
        liked_posts = get_likes_list(client, timestamp, limit=LIMIT)
        # print(liked_posts)

        if liked_posts:
            for index, post in enumerate(liked_posts):
                last_post = client.reblog(
                    BLOG_NAME, id=post["id"], reblog_key=post["reblog_key"],
                )
                logging.info(
                    f"{x*50 + index} - {post['blog_name']}: {post['post_url']} -- {post['liked_timestamp']}"
                )
                try:
                    post_id = last_post["id"]
                except Exception as cant_post:
                    logging.error("Failed to post")
                    logging.error(cant_post)

            timestamp = liked_posts[-1]["liked_timestamp"]
            # print("Any liked posts?")
            # # loop over the data and do your thing
            # for index, post in enumerate(liked_posts):
            #     print(f"{x*50 + index} - {post['blog_name']}: {post['post_url']}")
            #     client.reblog(
            #         BLOG_NAME, id=post["id"], reblog_key=post["reblog_key"],
            #     )
        else:
            logging.warning("No new liked posts")
            break

    logging.info(f"Last timestamp after this run - {timestamp}")

    write_timestamp_to_file(TIMESTAMP_FILE, timestamp)


if __name__ == "__main__":
    main()

