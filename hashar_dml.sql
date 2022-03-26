
DROP TABLE IF EXISTS JobOffer;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Employer;

create table if not exists Employee(
    id bigint primary key generated always as identity,
    name varchar(512) not null,
    login varchar(512) not null,
    pass varchar(512) not null,
    contact varchar(512) not null,
    price bigint not null,
    address varchar(512) not null,
    age int not null,
    gender char not null,
    average_rating real

);

create table if not exists Employer(
    id bigint primary key generated always as identity,
    name varchar(512) not null,
    login varchar(512) not null,
    pass varchar(512) not null,
    contact varchar(512) not null,
    address varchar(512) not null,
    average_rating real

);

create table if not exists JobOffer(
    id bigint generated always as identity,
    is_accepted bool,
    is_cancelled bool,
    is_pending bool,
    cancelled_by varchar(512),

    employee_id bigint,
    employer_id bigint,
    PRIMARY KEY(id),

    CONSTRAINT fk_employee
        FOREIGN KEY (employee_id)
        REFERENCES Employee(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_employer
        FOREIGN KEY (employer_id)
        REFERENCES Employer(id)
        ON DELETE CASCADE
)