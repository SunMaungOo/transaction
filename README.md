Write Ahead Log

[A,B,C]

Change C to D

Add C to log

change C to D

[A,B,D]

Commit

if log is deleted ==> commit success

========================

Implementation

[A,B,C]

change C to D

Add C position , C to log

Create a command which change C position , C data to D data

When commit
{

    Run all the commands (change C to D)

    return is log deleted
}

==============

Note : the data are change only when the commit is called.

Commit sucess mean the data are successfully updated.

If commit doesn't success , it ok. It ok when the data are not fully updated or
when the log file is not deleted.

Whatever happen when the program start , it search for log file.
It revert with the data from the log file whatever happen (even if it only fail to delete the log file and data are fully changed.).
It then delete the log file.

=================

