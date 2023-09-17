#!/usr/bin/perl
use strict;
use warnings;
open my $fh, "input_day10.txt" or die;

my %types = (")"=>"(","}"=>"{",">"=>"<","]"=>"[");
my %reverse_types = reverse (%types);
my %points = (")"=>3,"}"=>1197,">"=>25137,"]"=>57);

my $score = 0;
while (my $line = <$fh>) {
  chomp $line;
  my @stack;
  foreach my $c (split("",$line)) {
  #  print "@stack\n";
    if ( exists $types{$c}) {
      my $openning = pop(@stack);
      if ($openning ne $types{$c}) {
        print "ERROR: expected $reverse_types{$openning}, found $c\n";
        $score += $points{$c};
        last;
      }
    }
    else {
      push @stack,$c;
    }
  }
}

print "SCORE: $score\n";


__DATA__
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
