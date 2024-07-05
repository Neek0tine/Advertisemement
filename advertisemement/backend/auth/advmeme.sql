-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: Advertisemement
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audiencefeatures`
--

SET FOREIGN_KEY_CHECKS=0;

CREATE DATABASE Advertisemement;
use Advertisemement;

DROP TABLE IF EXISTS `audiencefeatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audiencefeatures` (
  `feature_id` int(11) NOT NULL AUTO_INCREMENT,
  `meme_id` int(11) DEFAULT NULL,
  `intended_audience` varchar(20) DEFAULT NULL,
  `tone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`feature_id`),
  KEY `meme_id` (`meme_id`),
  CONSTRAINT `audiencefeatures_ibfk_1` FOREIGN KEY (`meme_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `compositionfeatures`
--

DROP TABLE IF EXISTS `compositionfeatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compositionfeatures` (
  `feature_id` int(11) NOT NULL AUTO_INCREMENT,
  `meme_id` int(11) DEFAULT NULL,
  `number_of_panels` varchar(20) DEFAULT NULL,
  `type_of_images` varchar(20) DEFAULT NULL,
  `scale` varchar(20) DEFAULT NULL,
  `movement` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`feature_id`),
  KEY `meme_id` (`meme_id`),
  CONSTRAINT `compositionfeatures_ibfk_1` FOREIGN KEY (`meme_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `profile_id` int(11) NOT NULL,
  `post_url` varchar(255) DEFAULT NULL,
  `caption` text DEFAULT NULL,
  `likes` int(11) DEFAULT NULL,
  `date_posted` datetime DEFAULT NULL,
  `engagement` float DEFAULT NULL,
  `local_download_directory` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_id` (`profile_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3917 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `profile_pic_url` varchar(255) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `following` int(11) DEFAULT NULL,
  `bio` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subjectfeatures`
--

DROP TABLE IF EXISTS `subjectfeatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subjectfeatures` (
  `feature_id` int(11) NOT NULL AUTO_INCREMENT,
  `meme_id` int(11) DEFAULT NULL,
  `type_of_subject` varchar(20) DEFAULT NULL,
  `attributes_of_subject` varchar(20) DEFAULT NULL,
  `character_emotion` varchar(20) DEFAULT NULL,
  `contains_words` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`feature_id`),
  KEY `meme_id` (`meme_id`),
  CONSTRAINT `subjectfeatures_ibfk_1` FOREIGN KEY (`meme_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

SET FOREIGN_KEY_CHECKS=1;

-- Dump completed on 2024-04-22 21:52:13
