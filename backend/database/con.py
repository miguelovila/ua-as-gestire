import bcrypt
import os
import sqlite3
from cfg import *


def initializeDatabase():
  try:
    if not os.path.exists(STORAGE_PATH):
      os.makedirs(STORAGE_PATH)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
    """
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY,
				mec INTEGER NOT NULL,
				name TEXT NOT NULL,
				email TEXT NOT NULL,
				password TEXT NOT NULL,
				profile_picture TEXT NOT NULL
			);
		"""
    )
    cur.execute(
    """
			CREATE TABLE IF NOT EXISTS tokens (
				id INTEGER PRIMARY KEY,
				token TEXT NOT NULL,
				expiration INTEGER NOT NULL,
				user_id INTEGER NOT NULL
			);
		"""
    )
    cur.execute(
    """
			CREATE TABLE IF NOT EXISTS rooms (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL,
				description TEXT NOT NULL,
				image TEXT NOT NULL,
				capacity INTEGER,
				power_sockets INTEGER,
				computers INTEGER,
				oscilloscopes INTEGER,
				signal_generators INTEGER,
				multimeters INTEGER,
				sound_system INTEGER,
				projector INTEGER,
				whiteboard INTEGER,
				reservations TEXT NOT NULL
			);
		"""
    )
    cur.execute(
    """
			CREATE TABLE IF NOT EXISTS equipments (
				id INTEGER PRIMARY KEY,
				name TEXT NOT NULL,
				description TEXT NOT NULL,
				reservations TEXT NOT NULL,
				locker TEXT NOT NULL,
				image TEXT NOT NULL,
        available INTEGER NOT NULL
			);
		"""
    )
    cur.execute(
    """
			CREATE TABLE IF NOT EXISTS reservations (
				id INTEGER PRIMARY KEY,
				user_id INTEGER NOT NULL,
				room_id INTEGER NOT NULL,
				start_time INTEGER NOT NULL,
				end_time INTEGER NOT NULL,
				reason TEXT
			);    
		"""
    )
    cur.execute(
    """
			CREATE TABLE IF NOT EXISTS equipment_reservations (
				id INTEGER PRIMARY KEY,
				user_id INTEGER NOT NULL,
				equipment_id INTEGER NOT NULL,
				start_time INTEGER NOT NULL,
				end_time INTEGER NOT NULL,
				usage_place TEXT,
        observation TEXT
			);
		"""
    )
    con.commit()
    con.close()
  except sqlite3.Error as error:
    raise Exception("Error connecting to the database: ", error)


def executor(query, tupledata=None):
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
  if tupledata == None:
    cursor.execute(query)
  else:
    cursor.execute(query, tupledata)
  data = cursor.fetchall()
  connection.commit()
  connection.close()
  return data


def fillSampleUserData():
  if len(executor("SELECT * FROM users;")) > 0:
    return
  executor(
    """
			INSERT INTO users (mec, name, email, password, profile_picture)
			VALUES (107000, 'Dummy User Zero', 'du0@ua.pt', ?, 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand');
		""",
      (bcrypt.hashpw("du0".encode("utf-8"), bcrypt.gensalt()),),
  )
  executor(
    """
			INSERT INTO users (mec, name, email, password, profile_picture)
			VALUES (107001, 'Dummy User One', 'du1@ua.pt', ?, 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand');
		""",
      (bcrypt.hashpw("du1".encode("utf-8"), bcrypt.gensalt()),),
  )
  executor(
    """
			INSERT INTO users (mec, name, email, password, profile_picture)
			VALUES (107002, 'Dummy User Two', 'du2@ua.pt', ?, 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand');
		""",
      (bcrypt.hashpw("du2".encode("utf-8"), bcrypt.gensalt()),),
  )


def fillSampleRoomData():
  if len(executor("SELECT * FROM rooms;")) > 0:
    return
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.01', 'Teaching Laboratory', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F007%2F050%2Foriginal.jpg&width=1200', 20, 10, 10, 10, 10, 10, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.02', 'Videoconference Room', 'https://www.medicina.ulisboa.pt/sites/default/files/styles/imagem_larga/public/images-crop/2019-08/sala_49.jpg?itok=ubaeck6x', 60, 30, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.03', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.04', 'Teaching Laboratory', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F007%2F050%2Foriginal.jpg&width=1200', 20, 10, 10, 0, 0, 0, 0, 1, 1, '[]'); """
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.05', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 9, 3, 0, 0, 0, 0, 0, 0, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.06', 'Teaching Laboratory', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F007%2F050%2Foriginal.jpg&width=1200', 20, 10, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.07', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.19', 'Classroom', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F000%2F883%2Foriginal.jpg&width=1200', 40, 30, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.23', 'Teaching Laboratory', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F007%2F050%2Foriginal.jpg&width=1200', 20, 15, 10, 5, 5, 5, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.24', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.25', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.26', 'Classroom', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F000%2F883%2Foriginal.jpg&width=1200', 20, 10, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.27', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.28', 'Classroom', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F000%2F883%2Foriginal.jpg&width=1200', 20, 20, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.29', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.30', 'Classroom', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F000%2F883%2Foriginal.jpg&width=1200', 30, 25, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.32', 'Classroom', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F000%2F883%2Foriginal.jpg&width=1200', 20, 20, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('ANF IV', 'Auditorium', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBHn0ixd_qUQurWM3UvmTbVbej5sIKrKI0HLXGzljcOUmVzKy1-uh2wpX-tKBs8KzWxqg&usqp=CAU', 200, 70, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('ANF V', 'Auditorium', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBHn0ixd_qUQurWM3UvmTbVbej5sIKrKI0HLXGzljcOUmVzKy1-uh2wpX-tKBs8KzWxqg&usqp=CAU', 200, 70, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.01', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.02', 'Office', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAZokk8Z_AX5LAJ8FvxdMhLfO_NQLsGiSfkxP2GGpwam3U9tfzYf4_wr0km33DAmlZYkU&usqp=CAU', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.03', 'Teaching Lab', 'https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F007%2F050%2Foriginal.jpg&width=1200', 30, 25, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )


def fillSampleEquipmentData():
  if len(executor("SELECT * FROM equipments;")) > 0:
      return
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Oscilloscope', 'Oscilloscope', '[]', '1A', 'https://ce8dc832c.cloudimg.io/v7/_cdn_/E5/E3/B0/00/0/736862_1.jpg?width=640&height=480&wat=1&wat_url=_tme-wrk_%2Ftme_new.png&wat_scale=100p&ci_sign=f74748506adae0394e6be45b7f2dd989baeb5430', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Arduino UNO', 'Development Board & Kit', '[]', '1B', 'https://pt.farnell.com/productimages/large/en_GB/2075382-40.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Raspberry Pi 4B', 'Development Board & Kit', '[]', '1C', 'https://pt.farnell.com/productimages/large/en_GB/3051885-40.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Raspberry Pi 3B+', 'Development Board & Kit', '[]', '1D', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7MA4VYUaIIuhUl0mSJfKmI35CZX5KJG3Fag&usqp=CAU', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('DETPIC', 'Development Board', '[]', '2A', 'https://cdn.discordapp.com/attachments/921334981454860349/1113402454369914920/IMG_20230531_104337.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone IV', 'Development Board', '[]', '2B', 'https://cdn1.botland.de/51822-large_default/altera-cyclone-iv-ep4ce6-fpga-entwicklungsboard-waveshare-6483.jpg', 1);"""
  )
  executor(	
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone V', 'Development Board', '[]', '2C', 'https://ae01.alicdn.com/kf/H510607f5390949ffb44b296ea47faf67P/Altera-Cyclone-V-SoC-5CSXFC6D6F31C6N-FPGA-Entwicklung-bord-Altera-DE10-Standard-FPGA-Entwicklung-Kit.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone V', 'Development Board', '[]', '2D', 'https://ae01.alicdn.com/kf/H510607f5390949ffb44b296ea47faf67P/Altera-Cyclone-V-SoC-5CSXFC6D6F31C6N-FPGA-Entwicklung-bord-Altera-DE10-Standard-FPGA-Entwicklung-Kit.jpg', 1);"""
  )
