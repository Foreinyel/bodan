USE `soccer_data` ;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `round_txt` VARCHAR(45) NULL COMMENT '',
  `start_time` DATETIME NOT NULL COMMENT '',
  `home_txt` VARCHAR(45) NULL COMMENT '',
  `away_txt` VARCHAR(45) NULL COMMENT '',
  `home` VARCHAR(45) NULL COMMENT '',
  `away` VARCHAR(45) NULL COMMENT '',
  `home_short` VARCHAR(45) NULL COMMENT '',
  `away_short` VARCHAR(45) NULL COMMENT '',
  `home_goal` SMALLINT(5) NULL ,
  `away_goal` SMALLINT(5) NULL ,
  `home_standing_before` SMALLINT(5) NULL COMMENT '赛前排名',
  `away_standing_before` SMALLINT(5) NULL COMMENT '赛前排名',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_id` (`id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_team_standing`
-- Desc 赛前联赛积分排名
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_team_standing` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_team_standing` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联比赛ID',
  `type` VARCHAR(45) NULL COMMENT 'all/home/away:全部/主场排名/客场排名',
  `team_type` VARCHAR(45) null COMMENT 'home/away：主队/客队',
  `match_count` SMALLINT(5) NULL COMMENT '比赛总数',
  `win` SMALLINT(5) NULL COMMENT '胜场次数',
  `draw` SMALLINT(5) NULL COMMENT '平场次数',
  `lose` SMALLINT(5) NULL COMMENT '输场次数',
  `goals` SMALLINT(5) NULL COMMENT '进球数',
  `lost_goals` SMALLINT(5) NULL COMMENT '失球数',
  `total_goals` SMALLINT(5) NULL COMMENT '净进球数（进球数-失球数）',
  `marks` SMALLINT(5) NULL COMMENT '积分',
  `standing` SMALLINT(5) NULL COMMENT '排名',
  `win_rate` DECIMAL(8,4) NULL COMMENT '胜率',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_team_standing_id` (`id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_history`
-- Desc head to head
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_history` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_history` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联联赛ID',
  `league_name` VARCHAR(45) NULL COMMENT '联赛名称',
  `start_date` DATETIME NULL COMMENT '比赛日期',
  `history_url` VARCHAR(200) null COMMENT '比赛链接',
  `home` VARCHAR(45) NULL COMMENT '主队',
  `away` VARCHAR(45) NULL COMMENT '客队',
  `home_goal` SMALLINT(5) NULL COMMENT '',
  `away_goal` SMALLINT(5) NULL COMMENT '',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_history_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_recent`
-- Desc 近期战绩
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_recent` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_recent` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联联赛ID',
  `team_type` VARCHAR(45) NOT NULL COMMENT 'home/away:主场球队/客场球队',
  `recent_type` VARCHAR(45) NOT NULL COMMENT 'all/home_away:近十场全部比赛/近十场主（客）队主（客）场比赛',
  `league_name` VARCHAR(45) NULL COMMENT '联赛名称',
  `start_date` DATETIME NULL COMMENT '比赛日期',
  `recent_url` VARCHAR(200) null COMMENT '比赛链接',
  `home` VARCHAR(45) NULL COMMENT '主队',
  `away` VARCHAR(45) NULL COMMENT '客队',
  `home_goal` SMALLINT(5) NULL COMMENT '',
  `away_goal` SMALLINT(5) NULL COMMENT '',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_recent_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_ouzhi`
-- Desc 欧指
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_ouzhi` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_ouzhi` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联联赛ID',
  `comp` VARCHAR(45) NULL COMMENT '博彩公司或交易所',
  `win` DECIMAL(8,3) NULL COMMENT '胜',
  `draw` DECIMAL(8,3) null COMMENT '平',
  `lose` DECIMAL(8,3) NULL COMMENT '负',
  `returns` VARCHAR(45) NULL COMMENT '返还率',
  `kelly_win` DECIMAL(8,3) NULL COMMENT '',
  `kelly_draw` DECIMAL(8,3) NULL COMMENT '',
  `kelly_lose` DECIMAL(8,3) NULL COMMENT '',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_ouzhi_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_rangqiu`
-- Desc 让球
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_rangqiu` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_rangqiu` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联联赛ID',
  `comp` VARCHAR(45) NULL COMMENT '博彩公司或交易所',
  `handicap` DECIMAL(8,3) NULL COMMENT '让球数',
  `win` DECIMAL(8,3) NULL COMMENT '胜',
  `draw` DECIMAL(8,3) null COMMENT '平',
  `lose` DECIMAL(8,3) NULL COMMENT '负',
  `returns` VARCHAR(45) NULL COMMENT '返还率',
  `kelly_win` DECIMAL(8,3) NULL COMMENT '',
  `kelly_draw` DECIMAL(8,3) NULL COMMENT '',
  `kelly_lose` DECIMAL(8,3) NULL COMMENT '',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_rangqiu_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_daxiao`
-- Desc 大小球
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_daxiao` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_daxiao` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联联赛ID',
  `comp` VARCHAR(45) NULL COMMENT '博彩公司或交易所',
  `handicap` VARCHAR(45) NULL COMMENT '盘口',
  `over` DECIMAL(8,3) NULL COMMENT '',
  `under` DECIMAL(8,3) null COMMENT '',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_daxiao_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`match_500_bifen`
-- Desc 比分
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`match_500_bifen` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`match_500_bifen` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `match_id` BIGINT(20) UNSIGNED NOT NULL COMMENT '关联联赛ID',
  `comp` VARCHAR(45) NULL COMMENT '博彩公司或交易所',
  `one_zero` VARCHAR(45) NULL ,
  `two_zero` VARCHAR(45) NULL ,
  `two_one` VARCHAR(45) NULL ,
  `three_zero` VARCHAR(45) NULL ,
  `three_one` VARCHAR(45) NULL ,
  `three_two` VARCHAR(45) null,
  `four_zero` VARCHAR(45) null,
  `four_one` VARCHAR(45) null,
  `four_two` VARCHAR(45) null,
  `four_three` VARCHAR(45) null,
  `zero_one` VARCHAR(45) null,
  `zero_two` VARCHAR(45) null,
  `one_two` VARCHAR(45) null,
  `zero_three` VARCHAR(45) null,
  `one_three` VARCHAR(45) null,
  `two_three` VARCHAR(45) null,
  `zero_four` VARCHAR(45) null,
  `one_four` VARCHAR(45) null,
  `two_four` VARCHAR(45) null,
  `three_four` VARCHAR(45) null,
  `zero_zero` VARCHAR(45) null,
  `one_one` VARCHAR(45) null,
  `two_two` VARCHAR(45) null,
  `three_three` VARCHAR(45) null,
  `four_four` VARCHAR(45) null,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `match_500_bifen_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;

-- -----------------------------------------------------
-- Table `soccer_data`.`spider_crawl_err_urls`
-- Desc 异常
-- -----------------------------------------------------
DROP TABLE IF EXISTS `soccer_data`.`spider_crawl_err_urls` ;

CREATE TABLE IF NOT EXISTS `soccer_data`.`spider_crawl_err_urls` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `spider_name` VARCHAR(200) NOT NULL COMMENT '',
  `req_url` VARCHAR(200)  NOT NULL COMMENT '',
  `txt` BLOB NULL COMMENT '',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `spider_crawl_err_urls_id` (`id` ASC)
)ENGINE = InnoDB
  DEFAULT CHARACTER SET = utf8mb4;