#!/usr/bin/perl
use strict;
use warnings;

open my $fh, 'input_day15.txt' or die;

my $template = <$fh>;
chomp $template;
my @chars = split "",$template;
my %num_chars;
my $num_steps = 40;

my $pairs;
foreach my $i (0..scalar(@chars)-1) {
    $num_chars{$chars[$i]}++;
    next unless $i;
    $pairs->{$chars[$i-1].$chars[$i]}++;
}

my %rules;
while (my $line = <$fh>) {
    next unless $line =~ /^([A-Z]*)\s->\s([A-Z])/;
    $rules{$1} = $2;
}

# =====================================================
foreach my $i (1..$num_steps) {
    my $new_pairs;
    foreach my $pair (keys %rules) {
        next unless defined $pairs->{$pair};

        my $new_value = $rules{$pair};
        $num_chars{$new_value} = 0 unless $num_chars{$new_value};
        $num_chars{$new_value}+=$pairs->{$pair};
        
        my $p1 = substr($pair,0,1) . $new_value;
        my $p2 = $new_value . substr($pair,1,1);
        print "$p1,$p2\n";
        
        $new_pairs->{$p1} = 0 unless $new_pairs->{$p1};
        $new_pairs->{$p2} = 0 unless $new_pairs->{$p2};
        
        $new_pairs->{$p1} += $pairs->{$pair};
        $new_pairs->{$p2} += $pairs->{$pair};
        
    }
    
    $pairs = $new_pairs;
    print "\n\n";
    use Data::Dumper;print Dumper $pairs,\%num_chars;

}
my @nums = sort {$a<=>$b} values %num_chars;
use Data::Dumper; print Dumper\@nums;
print "FINAL ANSWER: ",$nums[-1]-$nums[0],"\n";

__DATA__
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
