
--DEATH DETAILS

-- DATA UNDERSTANDING
select * from Portfolio_Project..CovidDeaths$
order by 3,4


--CHANGING THE DATATYPE
alter table Portfolio_Project..CovidDeaths$
alter column total_cases float;

--total_cases vs total deaths
SELECT location, date ,total_deaths, total_cases, round((total_deaths/total_cases)*100,2) DeathPercentage
FROM Portfolio_Project..CovidDeaths$
where location='India'
order by 1,2

--total_cases vs population
SELECT location, date ,total_deaths, total_cases,population, (total_cases/population)*100 AffectedRate
FROM Portfolio_Project..CovidDeaths$
where location='India'
order by 1,2

--Highest Affected Rate
SELECT location, MAX(total_cases) HighestCases, MAX((total_cases/population))*100 AffectedRate
FROM Portfolio_Project..CovidDeaths$
where continent is not null
group by location
order by 3 desc


--Highest DeathRate in location
SELECT location, MAX(total_deaths) HighestDeaths, max(population) population, MAX((total_deaths/population))*100 DeathRate
FROM Portfolio_Project..CovidDeaths$
where continent is not null
group by location
order by 2 desc


--Highest Deathrate over Continent
SELECT continent, max(total_deaths) HighestDeaths
FROM Portfolio_Project..CovidDeaths$
where continent is not null
group by continent
order by 2 desc


--GLOBAL NUMBERS
SELECT sum(new_deaths) total_deaths, sum(new_cases) total_cases,  sum(new_deaths)/sum(new_cases) *100 DeathPercentage
FROM Portfolio_Project..CovidDeaths$
where continent is not null





--VACCINATION DETAILS
select * from Portfolio_Project..CovidVaccinations$
order by 3,4


--JOINING DEATH AND VACCINATION TABLES
select * 
from Portfolio_Project..CovidDeaths$ dea inner join Portfolio_Project..CovidVaccinations$ vac
on dea.date = vac.date and dea.location = vac.location



-- percentage of people in country Vaccinated
SELECT location, date,population, new_vaccinations,
SUM(cast(new_vaccinations as float)) over (partition by location order by location,date) totalvaccinationstilldate
FROM Portfolio_Project..CovidVaccinations$
where continent is not null
order by 1,2


	
-- Exploring CTE Tables
with ctetab (location, date,population,new_vaccinations,totalvaccinationstilldate)
as 
(
SELECT location, date,population, new_vaccinations,
SUM(new_vaccinations) over (partition by location order by location,date) totalvaccinationstilldate
FROM Portfolio_Project..CovidVaccinations$
where continent is not null
)
select *, ((totalvaccinationstilldate/population))*100 t 
from ctetab

--creating temp table
drop table if exists #temp
create table #temp(
location varchar(255), 
date datetime,
population int,
new_vaccinations float,
totalvaccinationstilldate float
)

insert into #temp 
SELECT location, date,population, new_vaccinations,
SUM(cast(new_vaccinations as float)) over (partition by location order by location,date) totalvaccinationstilldate
FROM Portfolio_Project..CovidVaccinations$
where continent is not null


--VIEW FOR VISUALIZATIONS


CREATE VIEW percentageofvaccinations 
as
SELECT location, date,population, new_vaccinations,
SUM(new_vaccinations) over (partition by location order by location,date) totalvaccinationstilldate
FROM Portfolio_Project..CovidVaccinations$
where continent is not null


--

