from __future__ import annotations

from typing import Dict

config_default: Dict = {
    "Apply_Config": False,
    "Configuration": {
        "Authentication": {
            "gofile_api_key": "",
            "gofile_website_token": "",
            "pixeldrain_api_key": "",
            "nudostar_username": "",
            "nudostar_password": "",
            "simpcity_username": "",
            "simpcity_password": "",
            "socialmediagirls_username": "",
            "socialmediagirls_password": "",
            "xbunker_username": "",
            "xbunker_password": "",
        },
        "Files": {
            "db_file": "download_history.sqlite",
            "errored_download_urls_file": "Errored_Download_URLs.csv",
            "errored_scrape_urls_file": "Errored_Scrape_URLs.csv",
            "input_file": "URLs.txt",
            "log_file": "downloader.log",
            "output_folder": "Downloads",
            "output_last_forum_post_file": "URLs_last_post.txt",
            "unsupported_urls_file": "Unsupported_URLs.csv",
        },
        "Forum_Options": {
            "output_last_forum_post": False,
            "scrape_single_post": False,
            "separate_posts": False,
        },
        "Ignore": {
            "exclude_videos": False,
            "exclude_images": False,
            "exclude_audio": False,
            "exclude_other": False,
            "ignore_cache": False,
            "ignore_history": False,
            "skip_hosts": [],
            "only_hosts": [],
        },
        "JDownloader": {
            "apply_jdownloader": False,
            "jdownloader_username": "",
            "jdownloader_password": "",
            "jdownloader_device": "",
        },
        "Progress_Options": {
            "hide_new_progress": False,
            "hide_overall_progress": False,
            "hide_forum_progress": False,
            "hide_thread_progress": False,
            "hide_domain_progress": False,
            "hide_album_progress": False,
            "hide_file_progress": False,
            "refresh_rate": 10,
            "visible_rows_threads": 2,
            "visible_rows_domains": 2,
            "visible_rows_albums": 2,
            "visible_rows_files": 10,
        },
        "Ratelimiting": {
            "connection_timeout": 15,
            "ratelimit": 50,
            "throttle": 0.5,
        },
        "Runtime": {
            "allow_insecure_connections": False,
            "attempts": 10,
            "block_sub_folders": False,
            "disable_attempt_limit": False,
            "include_id": False,
            "max_concurrent_threads": 0,
            "max_concurrent_domains": 0,
            "max_concurrent_albums": 0,
            "max_concurrent_downloads_per_domain": 4,
            "output_errored_urls": False,
            "output_unsupported_urls": False,
            "proxy": "",
            "remove_bunkr_identifier": False,
            "required_free_space": 5,
            "skip_download_mark_completed": False,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
        },
        "Sorting": {
            "sort_downloads": False,
            "sort_directory": "Sorted Downloads",
            "sorted_audio": "{sort_dir}/{base_dir}/Audio",
            "sorted_images": "{sort_dir}/{base_dir}/Images",
            "sorted_others": "{sort_dir}/{base_dir}/Other",
            "sorted_videos": "{sort_dir}/{base_dir}/Videos",
        },
    },
}
