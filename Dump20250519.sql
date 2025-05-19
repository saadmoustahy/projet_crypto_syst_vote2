-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: systeme_vote
-- ------------------------------------------------------
-- Server version	8.0.42

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
  `id` int NOT NULL AUTO_INCREMENT,
  `username` char(150) DEFAULT NULL,
  `password_hash` varchar(260) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','scrypt:32768:8:1$Ie5mTAkaYwz9yyRD$a37c957bc83641a43291bd18b793d9991c4b7749f2ffee68f9f0f77ce2e48b153d376d856ebf3edb257fe6d9ec63e47fafe8007db55f1606b6307f2bde1022d6');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidat`
--

DROP TABLE IF EXISTS `candidat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `id_election` int NOT NULL,
  `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_election` (`id_election`),
  CONSTRAINT `candidat_ibfk_1` FOREIGN KEY (`id_election`) REFERENCES `election` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidat`
--

LOCK TABLES `candidat` WRITE;
/*!40000 ALTER TABLE `candidat` DISABLE KEYS */;
INSERT INTO `candidat` VALUES (1,'Candidat A',1,'2025-05-05 12:19:34'),(2,'Candidat B',1,'2025-05-05 12:19:34'),(3,'Candidat C',1,'2025-05-05 12:19:34');
/*!40000 ALTER TABLE `candidat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `electeur`
--

DROP TABLE IF EXISTS `electeur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `electeur` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `cle_publique` text NOT NULL,
  `cle_symetrique_chiffree` text NOT NULL,
  `hash_identifiant` varchar(64) NOT NULL,
  `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `code_verif` char(10) DEFAULT NULL,
  `id_confirmation_vote` char(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hash_identifiant` (`hash_identifiant`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `id_confirmation_vote` (`id_confirmation_vote`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `electeur`
--

LOCK TABLES `electeur` WRITE;
/*!40000 ALTER TABLE `electeur` DISABLE KEYS */;
INSERT INTO `electeur` VALUES (6,'Q2345','sdmoustahy@gmail.com','Xv4UvMMs+vHBngjAvcTODm5HqXdjWr31obnGFqlZsB64bkK0P7KYd7hLbZKgnJHEAEs1awx7e8dYq+QXHPLRyg==','Wv+ajM7mKwkqOHNrUEQYadfGOjprPzZqSTWP1gEzsy8=','cf3ab32344244c5c008cfd4383c6be332affef6e6bd7efcaf6201fee2e76336c','2025-05-08 17:57:32','472462',NULL),(9,'D2673','moustahysaad960@gmail.com','VTAYGik+xazSMaPAjCwT5+9tupAklIEkC4vN51wteOjHTNxsg1sYd39DUQge3MaW3c37ZRgJDQjJAxuVaatMwA==','ChIwzK7VLsH4SIA9mPWwB7EUA3wdByf9LH5cLUjhG5M=','2d2c0398e34ed67c7d858533014c8426fd0e68f6c0e3d9e28817083e168c7695','2025-05-09 12:47:56','601891','VT-2025-33IAMWYS'),(10,'Q5678','cheikh.mokhtar3002@gmail.com','Tjq6DAKmomzLwzCSAyPfBEoQvbb53IeC+nJVu2euAY6QYUq5jnSS3X4yH95fb9L/0UrNVUbsoSTK7xi4vfev6w==','lx35FTtR34VsdWKMYVEfZzE1IKdt6oxhsi3mTUHcgbY=','67890ebf98b26b276e1d0f14eb6f1c36e519c3c714af01a3d6b6a483ed5ad17a','2025-05-12 15:54:05','820448','VT-2025-AD43WPV4'),(11,'Q1235','tilaouiayoub6@gmail.com','Nlfu9OT7GIKEy0yK3EVEQ8Cpk0+0VapoSD1w97UMZ+eCrXH31lJM7BrAUQQF0QUijJzOzG0sAXhhXoN7z3FyjA==','0uTMd2fEZZfJ81LwRzCrSntnKQstTliuCh2tKecaZu4=','734ba98b3905226797a225e6dfbff18f893a99779b5c050c5ebf4c555e26b141','2025-05-16 15:35:58','924180','VT-2025-PLRMPI0K');
/*!40000 ALTER TABLE `electeur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `election`
--

DROP TABLE IF EXISTS `election`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `election` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titre` varchar(255) NOT NULL,
  `date_debut` datetime NOT NULL,
  `date_fin` datetime NOT NULL,
  `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election`
--

LOCK TABLES `election` WRITE;
/*!40000 ALTER TABLE `election` DISABLE KEYS */;
INSERT INTO `election` VALUES (1,'Élection présidentielle','2025-01-01 00:00:00','2025-12-31 23:59:59','2025-05-05 12:19:34');
/*!40000 ALTER TABLE `election` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vote` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_election` int NOT NULL,
  `hash_electeur` varchar(64) NOT NULL,
  `vote_chiffre_asym` text NOT NULL,
  `signature` text NOT NULL,
  `iv_aes` varchar(32) NOT NULL,
  `date_vote` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_election` (`id_election`,`hash_electeur`),
  CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`id_election`) REFERENCES `election` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
INSERT INTO `vote` VALUES (1,1,'11bfb207a6af40b89d6f9fea27b5195675e39b3e90275c4269ae478ae5a32711','8f793b28dbd7c39da178b7efab13fd720a0fd14b18da405386e8cceceb73cdfc','dcbebe980bb3a5f18338f113427db3b3','1cd33d670539b1aac7899ac99bd98ea8','2025-05-05 13:29:26'),(2,1,'1841965633f1fc439c2abb7937a1384d87ef1e45620ffdc1cc915d454ecfbe4d','8f793b28dbd7c39da178b7efab13fd720a0fd14b18da405386e8cceceb73cdfc','dcbebe980bb3a5f18338f113427db3b3','16a79eb550524a605415d054f832c080','2025-05-05 13:32:37'),(3,1,'50bc1faa8d9c8253280de84a0ab454f2d6503c36568da5b323db28e15d0ded16','8f793b28dbd7c39da178b7efab13fd720a0fd14b18da405386e8cceceb73cdfc','dcbebe980bb3a5f18338f113427db3b3','8b1800cb123816fb9d9ffc259581a958','2025-05-05 13:45:10'),(8,1,'cf3ab32344244c5c008cfd4383c6be332affef6e6bd7efcaf6201fee2e76336c','87dcfa3fef4a5a2190a7cfea8019ec1f2901856729ffc38f56e7654c4f6f244e','d4c9b17637065f64d45051100116cb38','c92fb0419d594102a46d776527eb2208','2025-05-09 13:29:25'),(13,1,'2d2c0398e34ed67c7d858533014c8426fd0e68f6c0e3d9e28817083e168c7695','87dcfa3fef4a5a2190a7cfea8019ec1f2901856729ffc38f56e7654c4f6f244e','d4c9b17637065f64d45051100116cb38','15302a88cf8f7eae74fb1f72aa672c6b','2025-05-09 13:48:13'),(16,1,'67890ebf98b26b276e1d0f14eb6f1c36e519c3c714af01a3d6b6a483ed5ad17a','ca2b6e8eec5350e1aa5f305fe1d0e2d296dd69af20b70e37f870d213439b9ec8','ee6fa5adaed1f5dae31c2cd49c479013','8921536e57ea30e173dc4e2f7685bbae','2025-05-12 16:55:19'),(17,1,'734ba98b3905226797a225e6dfbff18f893a99779b5c050c5ebf4c555e26b141','ca2b6e8eec5350e1aa5f305fe1d0e2d296dd69af20b70e37f870d213439b9ec8','ee6fa5adaed1f5dae31c2cd49c479013','355796ffbd1aca2ac94855a468ff7885','2025-05-16 16:36:45');
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-19 11:59:00
