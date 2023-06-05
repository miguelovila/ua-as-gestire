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
			VALUES (107000, 'Dummy User Zero', 'du0@ua.pt', ?, 'http://gestire.miguelovila.com/api/images/student_1.png');
		""",
      (bcrypt.hashpw("du0".encode("utf-8"), bcrypt.gensalt()),),
  )
  executor(
    """
			INSERT INTO users (mec, name, email, password, profile_picture)
			VALUES (107001, 'Dummy User One', 'du1@ua.pt', ?, 'http://gestire.miguelovila.com/api/images/student_2.png');
		""",
      (bcrypt.hashpw("du1".encode("utf-8"), bcrypt.gensalt()),),
  )
  executor(
    """
			INSERT INTO users (mec, name, email, password, profile_picture)
			VALUES (107002, 'Dummy User Two', 'du2@ua.pt', ?, 'http://gestire.miguelovila.com/api/images/professor_1.png');
		""",
      (bcrypt.hashpw("du2".encode("utf-8"), bcrypt.gensalt()),),
  )


def fillSampleRoomData():
  if len(executor("SELECT * FROM rooms;")) > 0:
    return
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.01', 'Teaching Laboratory', 'http://gestire.miguelovila.com/api/images/lab1.jpg', 20, 10, 10, 10, 10, 10, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.02', 'Videoconference Room', 'http://gestire.miguelovila.com/api/images/sala_pc.jpg', 60, 30, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.03', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.04', 'Teaching Laboratory', 'http://gestire.miguelovila.com/api/images/resizer.jpeg', 20, 10, 10, 0, 0, 0, 0, 1, 1, '[]'); """
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.05', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 9, 3, 0, 0, 0, 0, 0, 0, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.06', 'Teaching Laboratory', 'http://gestire.miguelovila.com/api/images/lab1.jpg', 20, 10, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.07', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.19', 'Classroom', 'http://gestire.miguelovila.com/api/images/sala_aula.jpeg', 40, 30, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.23', 'Teaching Laboratory', 'http://gestire.miguelovila.com/api/images/lab1.jpg', 20, 15, 10, 5, 5, 5, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.24', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.25', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.26', 'Classroom', 'http://gestire.miguelovila.com/api/images/sala_aula.jpeg', 20, 10, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.27', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.28', 'Classroom', 'http://gestire.miguelovila.com/api/images/sala_aula.jpeg', 20, 20, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.29', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.30', 'Classroom', 'http://gestire.miguelovila.com/api/images/sala_aula.jpeg', 30, 25, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.1.32', 'Classroom', 'http://gestire.miguelovila.com/api/images/sala_aula.jpeg', 20, 20, 0, 0, 0, 0, 0, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('ANF IV', 'Auditorium', 'http://gestire.miguelovila.com/api/images/auditorio1.jpg', 200, 70, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('ANF V', 'Auditorium', 'http://gestire.miguelovila.com/api/images/auditorio.jpeg', 200, 70, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.01', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.02', 'Office', 'http://gestire.miguelovila.com/api/images/gabinete.jpeg', 6, 4, 0, 0, 0, 0, 0, 0, 0, '[]');"""
  )
  executor(
    """INSERT INTO rooms (name, description, image, capacity, power_sockets, computers, oscilloscopes, signal_generators, multimeters, sound_system, projector, whiteboard, reservations) VALUES ('4.2.03', 'Teaching Laboratory', 'http://gestire.miguelovila.com/api/images/resizer.jpeg', 30, 25, 0, 0, 0, 0, 1, 1, 1, '[]');"""
  )


def fillSampleEquipmentData():
  if len(executor("SELECT * FROM equipments;")) > 0:
      return
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Oscilloscope', 'Oscilloscope', '[]', '1A', 'http://gestire.miguelovila.com/api/images/osciloscopio.webp', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Arduino UNO', 'Development Board & Kit', '[]', '1B', 'http://gestire.miguelovila.com/api/images/arduino.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Raspberry Pi 4B', 'Development Board & Kit', '[]', '1C', 'http://gestire.miguelovila.com/api/images/raspberry.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('Raspberry Pi 3B+', 'Development Board & Kit', '[]', '1D', 'http://gestire.miguelovila.com/api/images/raspberry3b.jpeg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('DETPIC', 'Development Board', '[]', '2A', 'http://gestire.miguelovila.com/api/images/DETPIC.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone IV', 'Development Board', '[]', '2B', 'http://gestire.miguelovila.com/api/images/FPGA_IV.webp', 1);"""
  )
  executor(	
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone V', 'Development Board', '[]', '2C', 'http://gestire.miguelovila.com/api/images/FPGAV.jpg', 1);"""
  )
  executor(
    """INSERT INTO equipments (name, description, reservations, locker, image, available) VALUES ('FPGA Cyclone V', 'Development Board', '[]', '2D', 'http://gestire.miguelovila.com/api/images/FPGAV.jpg', 1);"""
  )
