package ru.itis.fillters;

import org.apache.commons.codec.digest.DigestUtils;
import ru.itis.hashfunctions.HashFunction;
import ru.itis.hashfunctions.HashFunctionWithParams;

import java.io.BufferedReader;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class CountableBloomFilter {
    private int cbf[];
    private List<HashFunction> hashFunctions;

    public CountableBloomFilter(final int sizeOfCbf, int numberOfHushFunction) {
        cbf = new int[sizeOfCbf];
        hashFunctions = new LinkedList<HashFunction>();
        hashFunctions.add(createOneTypeHashFunctions(numberOfHushFunction, sizeOfCbf));
    }

    public CountableBloomFilter(double p, int k, int m) {
        this((int) (-k * m / (Math.log(1 - Math.pow(p, 1.0 / k)))), k);
    }


    private HashFunction createOneTypeHashFunctions(Integer numberOfHushFunction, final Integer maxParam) {
        final List<Number> params = new ArrayList();
        for (int i = 0; i < numberOfHushFunction; i++) {
            params.add((int) (Math.random() * (maxParam - 1)));
        }
        HashFunction hashFunction = new HashFunctionWithParams(params) {

            public List<Integer> getIntHash(String string) {
                List<Integer> hashs = new ArrayList();
                for (Number n : params) {
                    boolean isnch = true;
                    int ch = 0;
                    int nch = 0;
                    String hash = DigestUtils.sha256Hex(string);
                    for (char c : hash.toCharArray()) {
                        if (isnch) {
                            nch += c;
                        } else {
                            ch += c;
                        }
                        isnch = !isnch;
                    }
                    hashs.add(((Integer) n * nch + (ch * ((Integer) n + 1)) + string.length()) % maxParam);
                }
                return hashs;
            }


        };

        return hashFunction;

    }

    public void study(BufferedReader reader) throws IOException {
        String line;
        while ((line = reader.readLine()) != null) {
            String[] words = line.split(" ");
            for (String word : words) {
                for (HashFunction function : hashFunctions) {
                    for (Integer hash : function.getIntHash(word)) {
                        cbf[hash]++;
                    }
                }
            }

        }
    }

    public boolean checkWord(String word) {
        for (HashFunction function : hashFunctions) {
            for (Integer hash : function.getIntHash(word)) {

                if (cbf[hash] == 0) {
                    return false;
                }
            }
        }


        return true;

    }
    public Boolean [] checkWords(String words[]) {
        ArrayList<Boolean> list = new ArrayList<Boolean>();
        for(String word:words){
            list.add(checkWord(word));
        }
        Boolean[] booleans = new Boolean[0];
        return  list.toArray(booleans);
    }


}
