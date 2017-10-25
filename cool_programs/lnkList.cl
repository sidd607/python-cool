class List {
	isNil():Bool {true};
	head(): Int { { abort(); 0; } };
	tail(): List { { abort(); self; } };
	add (i: Int) : List {
		(new Cons).init(i, self)
	};
};

class Cons inherits List {
	hd : Int;
	tl : List;
	hd : Int;
	isNil():Bool {false};
	head(): Int {hd};
	tail(): List {tl};
	init(i:Int, l: List):List{
		{
			hd <- i;
			tl <- l;
			self;
		}
	};
};

class Main inherits IO {

	mylist: List;

	print(i: List): Object{
		if i.isNil() then out_string("\n")
		else{
			print(i.tail());
			out_string(" ");
			out_int(i.head());
		}
		fi
	};

	main(): Object{
		{
			mylist <- new List.add(1).add(2).add(3).add(4);
			print(mylist);
			out_string("\n");
		}

	};
};
