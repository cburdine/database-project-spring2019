-- This is the curriculum basic dumping database file:

-- Dumping database structure for curricula_db
DROP DATABASE IF EXISTS `Curricula`;
CREATE DATABASE IF NOT EXISTS `Curricula` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Curricula`;

-- initialize `Person` table
DROP TABLE IF EXISTS `Person`;
CREATE TABLE IF NOT EXISTS `Person` (
	`id` int NOT NULL,
    `name` varchar(25) NOT NULL,
    PRIMARY KEY (`id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize 'Curriculum' table
DROP TABLE IF EXISTS `Curriculum`;
CREATE TABLE IF NOT EXISTS `Curriculum` (
	`name` varchar(25) NOT NULL,
    `min_credit_hours` int NOT NULL,
	`id_in_charge` int NOT NULL,
    PRIMARY KEY (`name`),
	FOREIGN KEY (`id_in_charge`) REFERENCES Person(`id`)
    /* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    
-- initialize 'Course' table
DROP TABLE IF EXISTS `Course`;
CREATE TABLE IF NOT EXISTS `Course` (
	`name` varchar(25) NOT NULL,
    `subject_code` varchar(4) NOT NULL,
    `credit_hours` int NOT NULL,
    `description` varchar(1023),
    PRIMARY KEY (`name`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `CurriculumListings` table
DROP TABLE IF EXISTS `CurriculumListings`;
CREATE TABLE IF NOT EXISTS `CurriculumListings` (
	`curriculum_name` varchar(25) NOT NULL,
    `course_name` varchar(25) NOT NULL,
    `required` boolean NOT NULL,
    PRIMARY KEY (`curriculum_name`,`course_name`),
	FOREIGN KEY (`curriculum_name`) REFERENCES Curriculum(`name`),
    FOREIGN KEY (`course_name`) REFERENCES Course(`name`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `Topic` table
DROP TABLE IF EXISTS `Topic`;
CREATE TABLE IF NOT EXISTS `Topic` (
	`id` int NOT NULL,
    `name` varchar(25) NOT NULL,
    PRIMARY KEY (`id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `CurriculumTopics` table
DROP TABLE IF EXISTS `CurriculumTopics`;
CREATE TABLE IF NOT EXISTS `CurriculumTopics` (
	`curriculum_name` varchar(25) NOT NULL,
    `topic_id` int NOT NULL,
    `level` int NOT NULL,
    `subject_area` varchar(127) NOT NULL,
    `time_unit` int NOT NULL,
    PRIMARY KEY (`curriculum_name`,`topic_id`),
	FOREIGN KEY (`curriculum_name`) REFERENCES Curriculum(`name`),
    FOREIGN KEY (`topic_id`) REFERENCES Topic(`id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `Section` table
DROP TABLE IF EXISTS `Section`;
CREATE TABLE IF NOT EXISTS `Section` (
	`course_name` varchar(25) NOT NULL,
    `semester` char NOT NULL,
    `unit_id` int NOT NULL,
    `num_students` int NOT NULL,
    `comment1` varchar(255),
    `comment2` varchar(255),
    PRIMARY KEY (`course_name`,`semester`,`unit_id`),
    FOREIGN KEY (`course_name`) REFERENCES Course(`name`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `SectionGrades` table
DROP TABLE IF EXISTS `SectionGrades`;
CREATE TABLE IF NOT EXISTS `SectionGrades` (
	`course` varchar(25) NOT NULL,
    `semester` char NOT NULL,
    `unit_id` int NOT NULL,
    
    `count_ap` int NOT NULL,
    `count_a` int NOT NULL,
    `count_am` int NOT NULL,
    
    `count_bp` int NOT NULL,
    `count_b` int NOT NULL,
    `count_bm` int NOT NULL,
    
    `count_cp` int NOT NULL,
    `count_c` int NOT NULL,
    `count_cm` int NOT NULL,
    
    `count_dp` int NOT NULL,
    `count_d` int NOT NULL,
    `count_dm` int NOT NULL,
    
    `count_i` int NOT NULL,
    `count_w` int NOT NULL,
    
    PRIMARY KEY (`course`,`semester`,`unit_id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `SectionGoalGrades` table
DROP TABLE IF EXISTS `SectionGoalGrades`;
CREATE TABLE IF NOT EXISTS `SectionGoalGrades` (
	`course` int NOT NULL,
    `semester` char NOT NULL,
    `unit_id` int NOT NULL,
    `goal_id` int NOT NULL,
    
    `count_ap` int NOT NULL,
    `count_a` int NOT NULL,
    `count_am` int NOT NULL,
    
    `count_bp` int NOT NULL,
    `count_b` int NOT NULL,
    `count_bm` int NOT NULL,
    
    `count_cp` int NOT NULL,
    `count_c` int NOT NULL,
    `count_cm` int NOT NULL,
    
    `count_dp` int NOT NULL,
    `count_d` int NOT NULL,
    `count_dm` int NOT NULL,
    
    PRIMARY KEY (`course`,`semester`,`unit_id`,`goal_id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `CourseTopics` table
DROP TABLE IF EXISTS `CourseTopics`;
CREATE TABLE IF NOT EXISTS `CourseTopics` (
	`course_name` varchar(25) NOT NULL,
    `topic_id` int NOT NULL,
    PRIMARY KEY (`course_name`,`topic_id`),
    FOREIGN KEY (`course_name`) REFERENCES Course(`name`),
    FOREIGN KEY (`topic_id`) REFERENCES Topic(`id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `Goal` table
DROP TABLE IF EXISTS `Goal`;
CREATE TABLE IF NOT EXISTS `Goal` (
	`id` int NOT NULL,
    `curriculum_name` varchar(25) NOT NULL,
    `description` varchar(255) NOT NULL,
    PRIMARY KEY (`id`,`curriculum_name`),
    FOREIGN KEY (`curriculum_name`) REFERENCES Curriculum(`name`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `CourseGoals` table
DROP TABLE IF EXISTS `CourseGoals`;
CREATE TABLE IF NOT EXISTS `CourseGoals` (
	`course_name` varchar(25) NOT NULL,
    `goal_id` int NOT NULL,
    PRIMARY KEY (`course_name`,`goal_id`),
	FOREIGN KEY (`course_name`) REFERENCES Course(`name`),
    FOREIGN KEY (`goal_id`) REFERENCES Goal(`id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


