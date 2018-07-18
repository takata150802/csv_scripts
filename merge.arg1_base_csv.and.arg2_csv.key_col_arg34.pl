#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

my $usage_msg = "
usage: \$ perl $0 csv1.csv csv2.csv 4 2
arg1: input file, base csv file
arg2: input file, csv file merged
arg3: parameter, column index of keys for base csv file
arg4: parameter, column index of keys for csv file merged
stdo: output csv file"; 

sub open_csv_file {
    my $file = shift;
    open my $fh, '<', $file
        or die "Cannot open '$file': $!";
    my $ret = []; 
    while (my $line = <$fh>) {
        chomp $line;
        my $items = []; 
        @$items = split(/,/, $line, -1); 
        push @$ret, $items;
        }
    close $fh;
    return $ret;
    }


### main
if ($#ARGV != (4-1)) {
    print $usage_msg . "\n";
    exit 1
    }
my ($path_to_base_csv, $path_to_merged_csv, $col_idx_base, $col_idx_merged) = @ARGV;


my @base_csv = open_csv_file($path_to_base_csv);
my $merged_csv = open_csv_file($path_to_merged_csv);
warn Dumper @base_csv;
warn Dumper $merged_csv;


for my $row ($merged_csv) {
    warn Dumper @$row[1];
    }
