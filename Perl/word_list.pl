# take in a text file and spit out the word usage, ranked
# so as to try and avoid repeating the same words constantly.
# does not consider phrases or n-grams however

open (FILE, "<./wordList.txt") || die $!;
open (OUT, ">./wordListOut.txt") || die $!;
while (<FILE>) {
	chomp;
	@line = split(" ");
	foreach $word (@line) {
		$word = lc($word);
		$word=~s/\.//;
		$word=~s/,//;
		$word=~s/;//;
		$dict{$word}++;
	}
}

foreach $key (sort hashValueDescendingNum (keys(%dict))) {
   print OUT "$dict{$key} \t\t $key\n";
}

sub hashValueDescendingNum {
   $dict{$b} <=> $dict{$a};
}
