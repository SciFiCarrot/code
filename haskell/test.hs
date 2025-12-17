double :: Int -> Int
double x = x * 2

sumTwo :: Int -> Int -> Int
sumTwo a b = a + b

main :: IO ()
main = do
    print (double 5)
    print (sumTwo 3 7)
    print ("Hello " ++ "world")
    print ([1,2,3] ++ [4,5])
