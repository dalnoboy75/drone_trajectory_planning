# 🚁 **Drone Trajectory Planning**

![GitHub stars](https://img.shields.io/github/stars/dalnoboy75/drone_trajectory_planning?style=social)
![GitHub forks](https://img.shields.io/github/forks/dalnoboy75/drone_trajectory_planning?style=social)
![GitHub license](https://img.shields.io/github/license/dalnoboy75/drone_trajectory_planning)

Добро пожаловать в проект **Drone Trajectory Planning**! Этот проект предназначен для построения кратчайшего маршрута для беспилотника с учетом возможных преград в виде окружностей и многоугольников.
## 📋 **Оглавление**

- [О проекте](#-о-проекте)
- [Возможности](#-возможности)
- [Команда](#-команда)
- [Технологии](#-технологии)
- [Установка](#-установка)
- [Использование](#-использование)
- [Примеры](#-примеры)
- [Контрибьюция](#-контрибьюция)
- [Лицензия](#-лицензия)

## 🌟 **О проекте**

> **Drone Trajectory Planning** — это проект, который решает задачу построения оптимального маршрута для беспилотника. Проект учитывает возможные преграды в виде окружностей и многоугольников, обеспечивая безопасное и эффективное движение.

### Основные задачи проекта:

- 🛰️ Построение кратчайшего маршрута.
- 🚧 Обход преград (окружностей и многоугольников).
- 🚀 Оптимизация пути с использованием алгоритмов Литтла и Дейкстры.

  ## ✨ **Возможности**

- 🛠️ **Алгоритмы Литтла и Дейкстры** для поиска и восстановления кратчайшего пути.
- 📐 **Геометрические расчеты** для обхода преград.
- 🖥️ **Графический интерфейс** для визуализации маршрута.
- 📊 Поддержка работы с данными в форматах CSV и JSON.

  ## 👥 **Команда**

Проект был реализован командой из трех человек:

| Имя           | Роль                                      | Контакты                          |
|---------------|-------------------------------------------|-----------------------------------|
| **Новиков Иван** | Алгоритмы (Литтла, Дейкстры)              | [GitHub](https://github.com/dalnoboy75) |
| **Большаков Матвей**    | Геометрическая часть (обход преград)       | [GitHub](https://github.com/Matvey-cmd)   |
| **Гостев Артём**    | Графический интерфейс (GUI)               | [GitHub](https://github.com/gulyonatyoma)  |


## 🛠️ **Технологии**

Проект разработан с использованием следующих технологий и библиотек:

- **PyQt5** — для создания графического интерфейса.
- **pyqtgraph** — для визуализации маршрута.
- **numpy** — для работы с матрицами и геометрическими расчетами.
- **csv, json, os, sys** — для работы с файлами и системными функциями.
- **matplotlib** — для дополнительной визуализации данных.
- [Doxygen](https://www.doxygen.nl/)

## 🚀 **Установка**

Чтобы установить проект, выполните следующие шаги:

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/dalnoboy75/drone_trajectory_planning.git
2. Перейдите в директорию проекта:

   ```bash
   cd drone_trajectory_planning
3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
4. Запустите проект

   ```bash
   python gui.py

## 🎮 **Использование**

1. Откройте приложение.
2. Загрузите данные о препятствиях (окружности, многоугольники) в формате JSON или CSV.
3. Настройте начальную и конечную точки маршрута.
4. Нажмите кнопку "Рассчитать маршрут".
5. Просмотрите оптимальный маршрут на графике.

## 📊 **Примеры**

### Пример 1: Обход окружности

![Example 1](https://via.placeholder.com/400x200?text=Example+1)

### Пример 2: Обход многоугольника

![Example 2](https://via.placeholder.com/400x200?text=Example+2)


## 🤝 **Контрибьюция**

Мы приветствуем вклад от сообщества! Если вы хотите внести свой вклад, пожалуйста, ознакомьтесь с [CONTRIBUTING.md](CONTRIBUTING.md) для получения дополнительной информации.

### Как внести вклад:

1. Форкните репозиторий.
2. Создайте новую ветку (`git checkout -b feature/AmazingFeature`).
3. Сделайте коммит ваших изменений (`git commit -m 'Add some AmazingFeature'`).
4. Запушьте ветку (`git push origin feature/AmazingFeature`).
5. Откройте Pull Request.

## 📄 **Лицензия**

Этот проект лицензирован под [MIT License](LICENSE).


## 📞 **Контакты**

Если у вас есть вопросы или предложения, свяжитесь с нами:

- Email: your.email@example.com
- GitHub: [dalnoboy75](https://github.com/dalnoboy75)
- Twitter: [@username](https://twitter.com/username)

## 📞 **Контакты**

Если у вас есть вопросы или предложения, свяжитесь с нами:

- Email: your.email@example.com
- GitHub: [dalnoboy75](https://github.com/dalnoboy75)
- Twitter: [@username](https://twitter.com/username)

### 📦 **Requirements**

Для работы проекта требуются следующие библиотеки:

```plaintext
PyQt5==5.15.9
pyqtgraph==0.12.4
numpy==1.21.4
matplotlib==3.4.3
