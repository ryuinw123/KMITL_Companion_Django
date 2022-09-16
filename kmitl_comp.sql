-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: shitduck.duckdns.org    Database: kmitl_comp
-- ------------------------------------------------------
-- Server version	5.5.5-10.9.2-MariaDB-1:10.9.2+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookmark`
--

DROP TABLE IF EXISTS `bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmark` (
  `bookmark_student_id` int(11) NOT NULL,
  `bookmark_marker_id` int(11) NOT NULL,
  `createtime` datetime DEFAULT NULL,
  PRIMARY KEY (`bookmark_student_id`,`bookmark_marker_id`),
  KEY `bookmark_marker_id_idx` (`bookmark_marker_id`),
  CONSTRAINT `bookmark_marker_id` FOREIGN KEY (`bookmark_marker_id`) REFERENCES `marker` (`marker_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `bookmark_student_id` FOREIGN KEY (`bookmark_student_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmark`
--

LOCK TABLES `bookmark` WRITE;
/*!40000 ALTER TABLE `bookmark` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text DEFAULT NULL,
  `comment_marker_id` int(11) DEFAULT NULL,
  `comment_student_id` int(8) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `comment_marker_id_idx` (`comment_marker_id`),
  KEY `comment_student_id_idx` (`comment_student_id`),
  CONSTRAINT `comment_marker_id` FOREIGN KEY (`comment_marker_id`) REFERENCES `marker` (`marker_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `comment_student_id` FOREIGN KEY (`comment_student_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_like` (
  `cl_comment_id` int(11) NOT NULL,
  `cl_student_id` int(8) NOT NULL,
  `createtime` datetime DEFAULT NULL,
  KEY `comment_student_id_idx` (`cl_student_id`),
  KEY `cl_comment_id_idx` (`cl_comment_id`),
  CONSTRAINT `cl_comment_id` FOREIGN KEY (`cl_comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `cl_student_id` FOREIGN KEY (`cl_student_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emergency`
--

DROP TABLE IF EXISTS `emergency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency` (
  `contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `contact_number` varchar(45) DEFAULT NULL,
  `contact_name` varchar(45) DEFAULT NULL,
  `contact_admin_username` varchar(255) DEFAULT NULL,
  `createdtime` datetime DEFAULT NULL,
  PRIMARY KEY (`contact_id`),
  KEY `contact_admin_username_idx` (`contact_admin_username`),
  CONSTRAINT `contact_admin_username` FOREIGN KEY (`contact_admin_username`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergency`
--

LOCK TABLES `emergency` WRITE;
/*!40000 ALTER TABLE `emergency` DISABLE KEYS */;
/*!40000 ALTER TABLE `emergency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_id` int(8) NOT NULL AUTO_INCREMENT,
  `eventname` varchar(255) NOT NULL,
  `starttime` datetime DEFAULT NULL,
  `endtime` datetime DEFAULT NULL,
  `description` text DEFAULT NULL,
  `student_id` int(8) DEFAULT NULL,
  `marker_id` int(8) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `student_id_idx` (`student_id`),
  KEY `marker_id_idx` (`marker_id`),
  CONSTRAINT `marker_id` FOREIGN KEY (`marker_id`) REFERENCES `marker` (`marker_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `student_id` FOREIGN KEY (`student_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issue` (
  `issue_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text DEFAULT NULL,
  `imageurl` longtext DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `issue_user_id` int(8) DEFAULT NULL,
  `issue_marker_id` int(11) DEFAULT NULL,
  `issue_approve_admin_username` varchar(255) DEFAULT NULL,
  `issue_broadcast_admin_username` varchar(255) DEFAULT NULL,
  `broadcasttime` datetime DEFAULT NULL,
  `approvetime` datetime DEFAULT NULL,
  PRIMARY KEY (`issue_id`),
  KEY `issue_user_id_idx` (`issue_user_id`),
  KEY `issue_marker_id_idx` (`issue_marker_id`),
  KEY `issue_approve_admin_username_idx` (`issue_approve_admin_username`),
  KEY `issue_broadcast_admin_username_idx` (`issue_broadcast_admin_username`),
  CONSTRAINT `issue_approve_admin_username` FOREIGN KEY (`issue_approve_admin_username`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `issue_broadcast_admin_username` FOREIGN KEY (`issue_broadcast_admin_username`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `issue_marker_id` FOREIGN KEY (`issue_marker_id`) REFERENCES `marker` (`marker_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `issue_user_id` FOREIGN KEY (`issue_user_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marker`
--

DROP TABLE IF EXISTS `marker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marker` (
  `marker_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `lat` decimal(10,0) DEFAULT NULL,
  `long` decimal(10,0) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `tag` varchar(45) DEFAULT NULL,
  `imageURL` longtext DEFAULT NULL,
  `enable` int(11) DEFAULT NULL,
  `created_admin_id` varchar(255) DEFAULT NULL,
  `created_user_id` int(8) DEFAULT NULL,
  `approve_admin_username` varchar(255) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `approvetime` datetime DEFAULT NULL,
  PRIMARY KEY (`marker_id`),
  KEY `created_admin_id_idx` (`created_admin_id`),
  KEY `created_user_id_idx` (`created_user_id`),
  KEY `approve_admin_username_idx` (`approve_admin_username`),
  CONSTRAINT `approve_admin_username` FOREIGN KEY (`approve_admin_username`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `created_admin_id` FOREIGN KEY (`created_admin_id`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `created_user_id` FOREIGN KEY (`created_user_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marker`
--

LOCK TABLES `marker` WRITE;
/*!40000 ALTER TABLE `marker` DISABLE KEYS */;
/*!40000 ALTER TABLE `marker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marker_like`
--

DROP TABLE IF EXISTS `marker_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marker_like` (
  `markerlike_student_id` int(11) NOT NULL,
  `markerlike_marker_id` int(11) NOT NULL,
  `createtime` datetime DEFAULT NULL,
  PRIMARY KEY (`markerlike_student_id`,`markerlike_marker_id`),
  KEY `markerlike_marker_id_idx` (`markerlike_marker_id`),
  CONSTRAINT `markerlike_marker_id` FOREIGN KEY (`markerlike_marker_id`) REFERENCES `marker` (`marker_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `markerlike_student_id` FOREIGN KEY (`markerlike_student_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marker_like`
--

LOCK TABLES `marker_like` WRITE;
/*!40000 ALTER TABLE `marker_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `marker_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `header` text DEFAULT NULL,
  `body` text DEFAULT NULL,
  `imageurl` longtext DEFAULT NULL,
  `createdtime` datetime DEFAULT NULL,
  `n_created_admin_username` varchar(255) DEFAULT NULL,
  `n_broadcast_admin_username` varchar(255) DEFAULT NULL,
  `broadcasttime` datetime DEFAULT NULL,
  PRIMARY KEY (`news_id`),
  KEY `n_created_admin_username_idx` (`n_created_admin_username`),
  KEY `n_broadcast_admin_username_idx` (`n_broadcast_admin_username`),
  CONSTRAINT `n_broadcast_admin_username` FOREIGN KEY (`n_broadcast_admin_username`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `n_created_admin_username` FOREIGN KEY (`n_created_admin_username`) REFERENCES `admin` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `permission_id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_student_id` int(8) DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  PRIMARY KEY (`permission_id`),
  KEY `permission_student_id_idx` (`permission_student_id`),
  CONSTRAINT `permission_student_id` FOREIGN KEY (`permission_student_id`) REFERENCES `user` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission_marker`
--

DROP TABLE IF EXISTS `permission_marker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission_marker` (
  `pm_permission_id` int(11) NOT NULL,
  `pm_maker_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pm_permission_id`),
  KEY `pm_marker_id_idx` (`pm_maker_id`),
  CONSTRAINT `pm_marker_id` FOREIGN KEY (`pm_maker_id`) REFERENCES `marker` (`marker_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pm_permission_id` FOREIGN KEY (`pm_permission_id`) REFERENCES `permission` (`permission_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission_marker`
--

LOCK TABLES `permission_marker` WRITE;
/*!40000 ALTER TABLE `permission_marker` DISABLE KEYS */;
/*!40000 ALTER TABLE `permission_marker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `student_id` int(8) NOT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `Student_Id_UNIQUE` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (99999999,'Banana','okok','banana@kmitl.ac.th','123456789');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-16 18:21:49
