# ST-StageTimeConvert
A python script to convert your sharptimer stage times into a csv for db upload.


Example usage from cmd:
`C:\Users\Marchand\Desktop\StageTimeConvert>python StageTimeConvert.py -i stagetimes`

Once you've upload the stage times to your db, run the following sql statement to update the empty PlayerName column:
```sql
UPDATE PlayerStageTimes AS pst
JOIN PlayerStats AS ps ON pst.SteamID = ps.SteamID
SET pst.PlayerName = ps.PlayerName;
```

![image](https://github.com/user-attachments/assets/cffbc598-6919-40a7-b308-754566f363cd)
![image](https://github.com/user-attachments/assets/e623f074-2479-41e3-9e45-0f4f4949c9e7)

