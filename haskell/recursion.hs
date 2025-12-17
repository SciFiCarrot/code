-- Main.hs
fak :: Int -> Int
fak t
  | t == 1 || t == 2 = 1
  | otherwise        = fak (t - 1) + fak (t - 2)

main :: IO ()
main = do
  print (fak 3)
  print (fak 2)
  print (fak 1)
  print (fak 0)  -- this will not terminate (like your JS)

