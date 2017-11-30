class Main inherits IO {
  tmp: Int;
  test: String;
  tmpo(x:Int): Int{
    x + tmp
  };

  main() : Object {{
    tmp <- 1;
    out_string("123"); 
    test <- tmpo(tmp);
  }};
};
