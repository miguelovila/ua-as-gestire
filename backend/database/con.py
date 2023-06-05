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
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.01', 'Teaching Laboratory', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/lab1.jpg?raw=true', 20, 10, 10, 10, 10, 10, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.02', 'Videoconference Room', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/sala_pc.jpg?raw=true', 60, 30, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.03', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.04', 'Teaching Laboratory', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/resizer.jpeg?raw=true', 20, 10, 10, 0, 0, 0, 0, 1, 1, '[]'); """
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.05', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 9, 3, 0, 0, 0, 0, 0, 0, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.06', 'Teaching Laboratory', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/lab1.jpg?raw=true', 20, 10, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.07', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.19', 'Classroom', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/sala_aula.jpeg?raw=true', 40, 30, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.23', 'Teaching Laboratory', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/lab1.jpg?raw=true', 20, 15, 10, 5, 5, 5, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.24', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.25', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.26', 'Classroom', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/sala_aula.jpeg?raw=true', 20, 10, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.27', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.28', 'Classroom', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/sala_aula.jpeg?raw=true', 20, 20, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.29', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.30', 'Classroom', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/sala_aula.jpeg?raw=true', 30, 25, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.32', 'Classroom', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/sala_aula.jpeg?raw=true', 20, 20, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('ANF IV', 'Auditorium', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/auditorio.jpeg?raw=true', 200, 70, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('ANF V', 'Auditorium', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/auditorio1.jpg?raw=true', 200, 70, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.01', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.02', 'Office', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/gabinete.jpeg?raw=true', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.03', 'Teaching Lab', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/resizer.jpeg?raw=true', 30, 25, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )


def fillSampleEquipmentData():
  if len(executor("SELECT * FROM equipments;")) > 0:
      return
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Oscilloscope', 'Oscilloscope', '[]', '1A', 'https://github.com/miguelovila/ua-as-gestire-project/raw/main/images/osciloscopio.webp', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Arduino UNO', 'Development Board & Kit', '[]', '1B', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/arduino.jpg?raw=true', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Raspberry Pi 4B', 'Development Board & Kit', '[]', '1C', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/raspberry.jpg?raw=true', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Raspberry Pi 3B+', 'Development Board & Kit', '[]', '1D', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/raspberry_3b.jpeg?raw=true', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('DETPIC', 'Development Board', '[]', '2A', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/DETPIC.jpg?raw=true', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone IV', 'Development Board', '[]', '2B', 'https://github.com/miguelovila/ua-as-gestire-project/raw/main/images/FPGA_IV.webp', 1);"""
  )
  executor(	
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone V', 'Development Board', '[]', '2C', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/FPGAV.jpg?raw=true', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone V', 'Development Board', '[]', '2D', 'https://github.com/miguelovila/ua-as-gestire-project/blob/main/images/FPGAV.jpg?raw=true', 1);"""
  )
