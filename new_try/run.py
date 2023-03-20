from pathlib import Path
from vunit import VUnit

vu = VUnit.from_argv()
# Add a library called "lib" to the project
lib = vu.add_library("lib")
lib.add_source_files(Path(__file__).parent / "*.vhd")

TB_GENERATED = lib.test_bench("my_array_tb")

for test in TB_GENERATED.get_tests():
    
    if test.name == "Test_with_loop":
        for i in range(0,4):
            for j in range(0,4):
                test.add_config(name = "loop_test: i: " + str(i) + " j: " + str(j),
                                generics = dict(rowing = i, coling = j)
                                )

    if test.name == "test_pass":
        
        test.add_config(name = "lasts",
                        generics = dict(rowing = 3, coling = 3),
                        #post_check=make_post_check(row, col),
                        )
    
    if test.name == "2nd test":
        test.add_config(name = "Middle",
                        generics = dict(rowing = 2, coling = 2),
                        #post_check=make_post_check(row, col),
                        )



# Run the test suite
vu.main()