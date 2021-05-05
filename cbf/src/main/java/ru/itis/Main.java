package ru.itis;

import ru.itis.fillters.CountableBloomFilter;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

public class Main {
    public static void main(String[] args) throws IOException {
        CountableBloomFilter filter = new CountableBloomFilter(0.0001,10,1816);
        BufferedReader reader = new BufferedReader(new FileReader("src\\main\\resources\\data\\post2.txt"));
        filter.study(reader);

        Boolean [] answers = filter.checkWords(
                new String[]{"def","научитесь:","спорт",
                        "отрывать","часовой","максимальный",
                        "странный","возвращать","аппарат",
                        "программный"});

        for(boolean b: answers){
            System.out.println(b);
        }

    }
}
