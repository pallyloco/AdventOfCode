#!/usr/bin/perl
use strict;
use warnings;
my $ONE = 2;
my $FOUR = 4;
my $SEVEN = 3;
my $EIGHT = 7;

my $sum = 0;
open my $fh, "input_day8.txt" or die;
foreach my $line (<$fh>) {
  print $line;
  my ($key,$digits) = split("\\|",$line);
  my @digits = split(" ",$digits);
  foreach my $digit (@digits) {
    my $len = length($digit);
    if ($len == $ONE || $len == $FOUR || $len == $SEVEN || $len==$EIGHT) {
      $sum++;
    }
  }
}
print "Sum is $sum\n" ;

__DATA__
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
