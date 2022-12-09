# BNR Crawler

<!-- ![web.jpeg](../images/../RadioTheaterCrawler/images/web.jpeg) -->

## Task
Да се извлекат публикациите в секцията "Любопитно", които са публикувани през последните 10 дни.
https://bnr.bg/hristobotev/knowledge/list?page_1_1=

Данните, които трябва да се съхранят в база данни (MySQL или MongoDB) са:

Име на новина
Дата на публикуване
Съдържание на новина
Да се състави потребителски интерфейс в който да се представят таблично получените данни.

Трябва да има поле за филтриране по дата на новина и възможност за сортиране (в намаляващ/увеличаващ ред) по име на новина.

## Install

1. Create virtual environment:

	open terminal in project root folder  and write:

	``python -m venv .venv``

2. Activate virtual environment:

	in CMD:

	`.venv\Scripts\activate.bat`

3. Install packages:

	`pip install -r requirements.txt`

4. Change config.ini

	In `lib/config.ini` set your MySQL username, password and DB name

5. Run App:

	`python app.py`

