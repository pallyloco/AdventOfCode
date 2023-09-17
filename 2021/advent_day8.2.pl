use strict;
use warnings;
open my $fh, "input_day8.txt" or die;

my $sum = 0;
while (my $line = <$fh>) {
  my ($key,$digits) = split("\\|",$line);
  my @keys = split(" ",$key);
  my $keys = decipher_keys(\@keys);
  my @digits = split(" ",$digits);
  my $output = decipher_data(\@digits,$keys);
  print "OUTPUT: $output\n";
  $sum += $output;
}
print "\nFINAL: $sum\n";

sub decipher_data {
  my $digits = shift;
  my $keys = shift;
  my $sum = 0;
  foreach my $digit (@$digits) {
    $sum = $sum*10 + $keys->{convert_string_tohashkey($digit)};
  }
  return $sum;
}



sub decipher_keys {
  my $unknowns = shift;
  my %keys;
  my %letters;

  # find all the easy ones
  my @one = grep {length($_) == 2} @$unknowns;
  my @four = grep {length($_) == 4} @$unknowns;
  my @seven = grep {length($_) == 3} @$unknowns;
  my @eight = grep {length($_) == 7} @$unknowns;

  $keys{1} = convert_string_tohashkey($one[0]);
  $keys{4} = convert_string_tohashkey($four[0]);
  $keys{7} = convert_string_tohashkey($seven[0]);
  $keys{8} = convert_string_tohashkey($eight[0]);
  $letters{a} = $keys{7} ^ $keys{1};

  # find the number 6
  my @sizesixes = grep {length($_) == 6} @$unknowns;
  my @six = grep {( convert_string_tohashkey($_) & $keys{1}) != $keys{1} } @sizesixes;
  $keys{6} = convert_string_tohashkey($six[0]);
  $letters{f} = $keys{6} & $keys{1};
  $letters{c} = $keys{8} ^ $keys{6};

  # find the number 9
  @sizesixes = grep {$_ ne $six[0]} @sizesixes;
  my @nine = grep { is_single_bit(
        ($letters{a}|$keys{4})^convert_string_tohashkey($_)
      )
    }
    @sizesixes;

  $keys{9} = convert_string_tohashkey($nine[0]);
  $letters{g} = ($letters{a}|$keys{4})^$keys{9};
  $letters{e} = $keys{8} ^ $keys{9};

  # find the number 0
  @one = grep {convert_string_tohashkey($_) != $keys{9}} @sizesixes;
  $keys{0} = convert_string_tohashkey($one[0]);
  $letters{b} = $keys{0}^($letters{a}|$letters{c}|$letters{e}|$letters{f}|$letters{g});

  # last position
  $letters{d} = $keys{8}^($letters{a}|$letters{b}|$letters{c}|$letters{e}|$letters{f}|$letters{g});

  # last numbers
  $keys{2} = $letters{a}|$letters{c}|$letters{d}|$letters{e}|$letters{g};
  $keys{3} = $letters{a}|$letters{c}|$letters{d}|$letters{f}|$letters{g};
  $keys{5} = $letters{a}|$letters{b}|$letters{d}|$letters{f}|$letters{g};

  %keys = reverse(%keys);
  return \%keys;
}

sub is_single_bit {
  my $num = shift;
  my $power = 1;
  foreach my $i (0..7) {
    return $num if $num == $power;
    $power = $power*2;
  }
  return 0;
}

sub convert_string_tohashkey {
  my $string = shift;
  my $number = 0;
  foreach my $c (split("",$string)) {
    $number += 2**(ord('g') - ord($c));
  }
  return $number;
}

__DATA__
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
