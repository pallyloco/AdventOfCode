#!/usr/bin/perl
use strict;
use warnings;
open my $fh, "input_day10.txt" or die;

my %points = (")"=>1,"}"=>3,">"=>4,"]"=>2);
my %types = (")"=>"(","}"=>"{",">"=>"<","]"=>"[");
my %reverse_types = reverse (%types);

my @scores;
while (my $line = <$fh>) {
  chomp $line;
  my @stack;
  my $valid = 1;
  foreach my $c (split("",$line)) {
  #  print "@stack\n";
    if ( exists $types{$c}) {
      my $openning = pop(@stack);
      if ($openning ne $types{$c}) {
        $valid = 0;
        last;
      }
    }
    else {
      push @stack,$c;
    }
  }

  # valid, but incomplete line
  # to complete, just keep popping the @stack
  if ($valid) {
    my $score = 0;
    while (my $openning = pop(@stack)) {
      $score = $score*5 + $points{$reverse_types{$openning}};
    }
    push @scores,$score;
  }
}

@scores = sort{$a<=>$b} @scores;
print "Middle score is : ",$scores[scalar(@scores)/2],"\n";


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
