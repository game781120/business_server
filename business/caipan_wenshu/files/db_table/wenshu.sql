/*
Navicat MySQL Data Transfer

Source Server         : 10.0.12.85
Source Server Version : 80033
Source Host           : 10.0.12.85:3306
Source Database       : wenshu

Target Server Type    : MYSQL
Target Server Version : 80033
File Encoding         : 65001

Date: 2024-04-12 21:13:33
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for wenshu
-- ----------------------------
DROP TABLE IF EXISTS `wenshu`;
CREATE TABLE `wenshu` (
  `uuid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `case_num` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '案号',
  `case_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '案件名称',
  `court` varchar(255) DEFAULT NULL COMMENT '法院',
  `area` varchar(255) DEFAULT NULL COMMENT '所属地区',
  `case_type` varchar(255) DEFAULT NULL COMMENT '案件类型',
  `case_type_code` int DEFAULT NULL COMMENT '案件类型编码',
  `source` varchar(255) DEFAULT NULL COMMENT '来源',
  `trial` varchar(255) DEFAULT NULL COMMENT '审理程序',
  `referee_date` varchar(255) DEFAULT NULL COMMENT '裁判日期',
  `public_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '公开日期',
  `case_personnel` varchar(255) DEFAULT NULL COMMENT '当事人',
  `case_reason` varchar(255) DEFAULT NULL COMMENT '案由',
  `legal_basis` varchar(4096) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '法律依据',
  `full_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '全文',
  `original_link` varchar(255) DEFAULT NULL COMMENT '原始链接',
  PRIMARY KEY (`uuid`),
  FULLTEXT KEY `case_num_name` (`case_num`,`case_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
