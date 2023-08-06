# CompressBinaryTable
 
## Basic Usage:

```console
cbt -i input_file -o output_file -c 
```

## Options:

```console
-i = input, required 
-o = output, required 
-c = compression 
-d = decompression 
-t = output type, either csv or tsv 
--override = to override output file if it exist 
```

## Available Python functions:

```
# Returns numpy array of file as uncompressed, useful for ML (same as load as pandas df, and to_numpy())
cbt_to_array(compressed_file)

# Returns numpy array of name of the mutations as uncompressed, useful for ML, (same as load pandas df and use df.colums)
cbt_columns(compressed_file)
```

## Required file example:

### CSV:

```
strain_name,mut1,mut2,mut3,mut4,outcome
strain1,0,1,1,1,1,1
strain2,0,0,1,1,1,0
strain3,0,1,0,1,1,0
strain4,1,1,1,1,1,1
```

### TSV:

```
strain_name mut1    mut2    mut3    mut4    outcome
strain1 0   1   1   1   1   1
strain2 0   0   1   1   1   0
strain3 0   1   0   1   1   0
strain4 1   1   1   1   1   1
```

### CBT:

```
1;mut1;mut2;mut3;mut4;outcome
strain1;6;43;87;102
strain2;16;43;87;102
strain3;6;53;78;112
strain4;61;413;824;942
```



