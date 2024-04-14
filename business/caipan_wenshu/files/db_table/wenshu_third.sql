-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: db_name_001
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `wenshu_third`
--

DROP TABLE IF EXISTS `wenshu_third`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wenshu_third` (
  `uuid` varchar(255) NOT NULL,
  `type` int DEFAULT NULL COMMENT '案件类型',
  `type_name` varchar(255) DEFAULT NULL COMMENT '案件类型名称',
  `parent_type` int DEFAULT NULL COMMENT '父类型',
  `money` int DEFAULT '0' COMMENT '涉案现金',
  `is_money` int DEFAULT NULL COMMENT '是否提取了涉案金额',
  `article` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '涉案物品',
  `is_article` int DEFAULT NULL COMMENT '是否提取了涉案物品',
  `article_money` int DEFAULT '0',
  `case_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作案时间',
  `case_personnel` varchar(255) DEFAULT NULL COMMENT '作案人员',
  `personnel_career` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作案人员职业',
  `case_tool` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作案工具',
  `location` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '地点',
  `judgment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '判决',
  `punish_money` int DEFAULT '0' COMMENT '处罚金额',
  `zishou` varchar(255) DEFAULT NULL COMMENT '自首',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-05  7:12:28
