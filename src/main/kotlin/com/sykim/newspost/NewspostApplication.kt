package com.sykim.newspost

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class NewspostApplication

fun main(args: Array<String>) {
	runApplication<NewspostApplication>(*args)
}
