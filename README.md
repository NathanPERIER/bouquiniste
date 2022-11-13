# Bouquiniste

Bouquiniste is a script that aims to fetch books to be published on dedicated sites and send notifications for the series you follow.

## Configuration

TODO

## Usage

You call the script by giving it a time period (starting from the current date) for which it will get all the books and select only those you are intereted in. You can specify a certain number of months, weeks and days in the future, as following :

```
./bouquiniste.py 1m1w1d
```

You don't need to specify the 0s, but the values must be given in the correct order :

```
./bouquiniste.py 3w1d
```

The idea is to put this in a cron tab, where the duration between two calls of the script is smaller than the time period given as an argument. In the vast majority of cases, making more than one refresh per day will not change anyhting.

## Source

| identifier   | site                                          | language(s) |
|--------------|-----------------------------------------------|-------------|
| `manga_news` | [manga-news.com](https://www.manga-news.com/) | fr          |

## Notifiers

| identifier | app                             |
|------------|---------------------------------|
| `discord`  | [Discord](https://discord.com/) |
