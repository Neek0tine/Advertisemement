__author__ = "Nicholas Juan K. P."
__copyright__ = "Copyright 2024, The Advertisemement"
__credits__ = ["Mohammad Ghani", "Muhammad Noor Fakhruzzaman", "Nicholas Juan K. P."]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Nicholas Juan Kalvin P."
__email__ = "nicholas.juan.kalvin-2020@ftmm.unair.ac.id"
__status__ = "Development"

import instaloader
import time, os, random
import mysql.connector
import pandas as pd
import logging
from colorlog import ColoredFormatter   
from tqdm import tqdm
from PIL import Image                 
import requests                    
import time
import re
import glob
import csv

# Instaloader session
instaloader_session_user = 'neekjk'
dbname = 'advertisemement'

# Configure logger

logging.basicConfig(filename='src/instaloader.log',
                    filemode='a',
                    level=logging.DEBUG) 
logger = logging.getLogger('Instascraper') 

LOG_COLORS = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'warningING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red'}
FORMATTER = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(cyan)s%(asctime)s%(reset)s - %(message)s",
    datefmt='%H:%M:%S',
    log_colors=LOG_COLORS)

console_handler = logging.StreamHandler()
console_handler.setFormatter(FORMATTER)
logger.addHandler(console_handler)

class Instacrap:
    def __init__(self, session_user=instaloader_session_user):
        try:
            self.user = os.environ['instagram_username']
            self.passw = os.environ['instagram_password']
            self.db_user = os.environ['sql_username']
            self.db_passw = os.environ['sql_password']
            logger.info('Environment variables OK')
        except BaseException as e:
            logger.error(e, "Credentials are not found in system environment variables.")

        self.sql = mysql.connector.connect(host='127.0.0.1',user=self.db_user, passwd=self.db_passw)
        logger.info('Connection to MySQL OK')
        self.cursor = self.sql.cursor()
        
        self.cursor.execute(f'use {dbname}')
        logger.info(f'Using database: {dbname}')
        self.L = instaloader.Instaloader()

        try:
            self.L.load_session_from_file(session_user) 
            logger.info(f'Using saved Instaloader session: {instaloader_session_user}')
            return
        except:
            logger.warning('Fail to login using saved Instaloader session, attempting to login using saved environment variables')
            self.L.login(self.user, self.passw)
            logger.warning('Fail to login using saved environment variables, attempting to login manually')
            self.L.interactive_login(input('Username:'))

    @staticmethod
    def sleep():
        time.sleep(random.random() + random.randint(5,10))

    def scrape_profile_data(self, target_username):
        profile = instaloader.Profile.from_username(self.L.context, target_username)
        logger.info(f'Scraping profile: {target_username}')
        
        # # Print profile information
        print()
        print('==================== Profile Data =====================')
        print("Username:", profile.username)
        print("Full Name:", profile.full_name)
        
        print("Followers:", profile.followers)
        print("Following:", profile.followees)
        print("Bio:", profile.biography)
        _pp_url = profile.profile_pic_url
        print()
        print('==================== Saving Data =====================')

         # Check if profile already exists in database
        self.cursor.execute("SELECT * FROM profiles WHERE username = %s", (profile.username,))
        existing_profile = self.cursor.fetchone()
        if existing_profile:
            logger.info('Profile already exists in database')
            return
        
        logger.info('Attempting to save data to MySQL Database')
        self.cursor.execute(f"USE {dbname}")
        _info_table = "INSERT INTO profiles (username, full_name, profile_pic_url, followers, following, bio) VALUES (%s, %s, %s, %s, %s, %s)"
        _val = (profile.username, profile.full_name, _pp_url, profile.followers, profile.followees, profile.biography)
        self.cursor.execute(_info_table, _val)
        self.sql.commit()
        logger.info('Profile data inserted into database')

        # profile_pic_url = profile.profile_pic_url
        # try:
        #     response = requests.get(profile_pic_url, stream=True)
        #     image = Image.open(response.raw)
        #     image.show()
        #     logger.debug('Profile picture displayed')
        # except Exception as e:
        #     logger.error('Failed to display profile picture: %s', str(e))
    def scrape_posts(self, target_username):
        profile = instaloader.Profile.from_username(self.L.context, target_username)
        logger.info(f'Scraping posts of profile: {target_username}')

        # Retrieve the profile ID corresponding to the username
        self.cursor.execute("SELECT id FROM profiles WHERE username = %s", (profile.username,))
        profile_id_row = self.cursor.fetchone()
        if profile_id_row:
            profile_id = profile_id_row[0]
        else:
            logger.error(f'Profile ID for username {profile.username} not found in database')
            return

        _total_posts = profile.mediacount
        # Query database for total number of posts associated with the Instagram account
        self.cursor.execute("SELECT COUNT(*) FROM posts WHERE profile_id = %s", (profile_id,))
        _acquired = self.cursor.fetchone()[0]

        # Replace dots in the username with underscores in the directory name
        target_username_cleaned = re.sub(r'\.', '_', target_username)

        # Create directory for the user
        user_directory = os.path.join(os.getcwd(), "scraps", target_username_cleaned)
        os.makedirs(user_directory, exist_ok=True)
        posts_directory = os.path.join(user_directory, "posts")
        os.makedirs(posts_directory, exist_ok=True)
        
        # Redownload posts if they are not found in the expected folder
        for i, post in enumerate(tqdm(profile.get_posts(), total=_total_posts, desc='Scraping Posts')):
            post_directory = os.path.join(posts_directory, str(post.mediaid))
            if not os.path.exists(post_directory):
                try:
                    # Download the entire post
                    self.L.download_post(post, target=post_directory)
                    logger.info(f"Post {post.mediaid} downloaded successfully")

                    # Extract caption from the downloaded .txt file
                    caption_files = glob.glob(os.path.join(post_directory, '*.txt'))
                    if caption_files:
                        with open(caption_files[0], "r", encoding="utf-8") as f:
                            caption = f.read()
                    else:
                        caption = None

                    # Parse metadata from the downloaded .json.xz file
                    metadata_files = glob.glob(os.path.join(post_directory, '*.json.xz'))
                    if metadata_files:
                        metadata = instaloader.load_structure_from_file(self.L.context, metadata_files[0])
                        likes = metadata.likes
                        comments = metadata.comments
                        _post_date = metadata.date_utc
                    else:
                        likes = None
                        comments = None
                        _post_date = None

                    # Calculate engagement rate
                    engagement = (likes + comments) / profile.followers if profile.followers > 0 else 0.0

                    # Construct post URL
                    post_url = f"https://www.instagram.com/p/{post.shortcode}/"

                    # Insert post data into database
                    self.cursor.execute(f"USE {dbname}")
                    post_table = "INSERT INTO posts (post_id, username, profile_id, post_url, caption, likes, date_posted, engagement, local_download_directory) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (post.mediaid, profile.username, profile_id, post_url, caption, likes,
                            _post_date, engagement, post_directory)
                    self.cursor.execute(post_table, val)
                    self.sql.commit()
                    logger.info(f'Post with ID {post.mediaid} inserted into database')
                    self.sleep()  # Sleep for random duration to avoid rate limits
                except Exception as e:
                    logger.error(f"Failed to download post {post.mediaid}: {str(e)}")
            else:
                logger.info(f"Post {post.mediaid} already exists. Skipping...")

    def export_sql_data_to_csv(self, target_username):
        # Create directory for the user
        user_directory = os.path.join(os.getcwd(), "scraps", target_username)
        os.makedirs(user_directory, exist_ok=True)
        
        # Export profile data to CSV
        profile_csv_path = os.path.join(user_directory, "profile.csv")
        with open(profile_csv_path, 'w', newline='', encoding='utf-8') as csvfile:  # Specify UTF-8 encoding
            writer = csv.writer(csvfile)
            writer.writerow(['username', 'full_name', 'profile_pic_url', 'followers', 'following', 'bio'])
            self.cursor.execute("SELECT * FROM profiles WHERE username = %s", (target_username,))
            for row in self.cursor.fetchall():
                writer.writerow(row)
        logger.info(f"Profile data exported to {profile_csv_path}")

        # Export posts data to CSV
        posts_csv_path = os.path.join(user_directory, "posts.csv")
        with open(posts_csv_path, 'w', newline='', encoding='utf-8') as csvfile:  # Specify UTF-8 encoding
            writer = csv.writer(csvfile)
            writer.writerow(['post_id', 'username', 'profile_id', 'post_url', 'caption', 'likes', 'date_posted', 'engagement', 'local_download_directory'])
            self.cursor.execute("SELECT * FROM posts WHERE username = %s", (target_username,))
            for row in self.cursor.fetchall():
                writer.writerow(row)
        logger.info(f"Posts data exported to {posts_csv_path}")

    def scrap(self, target_username):
        self.scrape_profile_data(target_username)
        self.scrape_posts(target_username)
        self.export_sql_data_to_csv(target_username)
        logger.info('Scraping completed')
        return

if __name__ == "__main__":
    i = Instacrap()
    brands_list = ["grabid"]
    for brand in brands_list:
        i.scrap(brand)
    # i.export_sql_data_to_csv('memecomic.id')
    
