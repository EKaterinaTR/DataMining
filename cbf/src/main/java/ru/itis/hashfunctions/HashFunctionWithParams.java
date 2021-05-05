package ru.itis.hashfunctions;

import java.util.List;

public abstract class HashFunctionWithParams implements HashFunction {
   List<Number> params;
   public HashFunctionWithParams(List<Number> params){
       this.params = params;
   }
}
