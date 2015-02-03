CREATE DATABASE IF NOT EXISTS fnat_base;

USE fnat_base;

CREATE TABLE IF NOT EXISTS fnat_execution(
    exec_id      BIGINT    NOT NULL PRIMARY KEY AUTO_INCREMENT,
    build_number CHAR(50)  NOT NULL,
    start_time   DATETIME  NOT NULL,
    serial_no    CHAR(20)  NOT NULL,
    log_location CHAR(100) NOT NULL);

CREATE TABLE IF NOT EXISTS fnat_case_result(
    record_id BIGINT   NOT NULL PRIMARY KEY AUTO_INCREMENT,
    exec_id   BIGINT   NOT NULL,
    case_name CHAR(80) NOT NULL,
    verdict   CHAR     NOT NULL);
    
