# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import os

class PornPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.sqliteConnection = sqlite3.connect('database.db')
            self.cursor = self.sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_table(self):
        self.cursor.execute(""" DROP TABLE IF EXISTS flyingjizz_babes_data """)
        self.cursor.execute(""" CREATE TABLE flyingjizz_babes_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                thumbnail_link TEXT,
                                video_link TEXT,
                                video_location TEXT) """
                            )
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        insert_query = """INSERT INTO flyingjizz_babes_data
                          (title, thumbnail_link, video_link, video_location) 
                          VALUES (?, ?, ?, ?);"""
        insertable_data = (
            item['title'],
            item['thumbnail_link'],
            item['video_link'],
            item['video_location'],
        )
        self.cursor.execute(insert_query,insertable_data)
        self.sqliteConnection.commit()

    def store_to_s3bucket(self, item):
        command = f"wget -qO- { item['video_location'] } | aws s3 cp - s3://flyingjizz/{item['title']} "
        os.system(command)

    def close_spider(self, spider):
        self.sqliteConnection.close()