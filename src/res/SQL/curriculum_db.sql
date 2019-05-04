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
DELETE FROM `Person`;
INSERT INTO `Person` (`id`, `name`) VALUES
(1, 'John Doe'),
(2, 'Jane Doe');

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
DELETE FROM `Curriculum`;
INSERT INTO `Curriculum` (`name`, `min_credit_hours`,`id_in_charge`) VALUES
('Mathematics', 60, 1),
('Computer Science', 64, 2),
('Electrical Engineering', 62, 2);

    
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
INSERT INTO `Course` (`name`, `subject_code`,`credit_hours`,`description`) VALUES
('Intro to CS I', 'CSI-1420', 4, 'Do computer stuff'),
('Intro to CS II', 'CSI-1430', 4, 'Do more computer stuff'),
('Intro to EE','EGR-1400', 4, 'Learn about EE stuff'),
('Calculus I','MTH-1302', 3, 'Basics of calculus');

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
INSERT INTO `CurriculumListings` (`curriculum_name`, `course_name`,`required`) VALUES
('Computer Science', 'Intro to CS I', true),
('Computer Science', 'Intro to CS II',false),
('Electrical Engineering','Intro to EE',true),
('Mathematics','Calculus I',true);

-- initialize `Topic` table
DROP TABLE IF EXISTS `Topic`;
CREATE TABLE IF NOT EXISTS `Topic` (
	`id` int NOT NULL,
    `name` varchar(25) NOT NULL,
    PRIMARY KEY (`id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
INSERT INTO `Topic` (`id`, `name`) VALUES
(0, 'C++ programing'),
(1, 'C Programming'),
(2, 'Circuits'),
(3, 'Design'),
(4, 'Boolean Logic'),
(5, 'Derivatives'),
(6, 'Integrals');

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
INSERT INTO `CurriculumTopics` (`curriculum_name`, `topic_id`,`level`,`subject_area`,`time_unit`) VALUES
('Computer Science', 0, 1, 'programming', 4),
('Computer Science', 1, 2, 'advanced programming', 4),
('Electrical Engineering', 2, 2, 'circuits and hardware', 4),
('Electrical Engineering', 3, 1, 'design projects', 4),
('Electrical Engineering', 4, 1, 'math skills', 2),
('Mathematics', 5, 1, 'foundational calculus', 2),
('Mathematics', 6, 2, 'foundational calculus', 2);

-- initialize `Section` table
DROP TABLE IF EXISTS `Section`;
CREATE TABLE IF NOT EXISTS `Section` (
	`course_name` varchar(25) NOT NULL,
    `semester` char NOT NULL,
    `section_id` int NOT NULL,
    `num_students` int NOT NULL,
    `comment1` varchar(255),
    `comment2` varchar(255),
    PRIMARY KEY (`course_name`,`semester`,`section_id`),
    FOREIGN KEY (`course_name`) REFERENCES Course(`name`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `SectionGrades` table
DROP TABLE IF EXISTS `SectionGrades`;
CREATE TABLE IF NOT EXISTS `SectionGrades` (
	`course` varchar(25) NOT NULL,
    `semester` char NOT NULL,
    `section_id` int NOT NULL,
    
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
    
    PRIMARY KEY (`course`,`semester`,`section_id`)
	/* Add foreign key constraints*/
    
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- initialize `SectionGoalGrades` table
DROP TABLE IF EXISTS `SectionGoalGrades`;
CREATE TABLE IF NOT EXISTS `SectionGoalGrades` (
	`course` int NOT NULL,
    `semester` char NOT NULL,
    `section_id` int NOT NULL,
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
    
    PRIMARY KEY (`course`,`semester`,`section_id`,`goal_id`)
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


