import sys
import time
import datetime as dt
import pymysql as pm
import prettytable as pt
#=============================================================================================
#GLOBAL VARIABLES
usr='root'
pwd='root'
db='bms'
gapvalue=30
#=============================================================================================
def maxtid():
    maxtid=''
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        qry="select max(Tid) from TRANSACTION"
        cur.execute(qry) 
        row=cur.fetchone() #(None,)
        #print(row)    
        if row[0]==None:
            maxtid=1000
            
        else:
            maxtid=int(row[0])+1
        
               
    except pm.DatabaseError as e:
        con.rollback()
        print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
    return maxtid
#==============================================================================================
def add_transaction(Acno,a,blnc,b):
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
       #=============================================================================
        if a==1:
             qry=f"INSERT INTO TRANSACTION VALUES('{maxtid()}','{b}','{Acno}','{dt.datetime.today()}','{'Deposit'}','{blnc}')"
             
             cur.execute(qry)
             con.commit()
        elif a==2:
             qry=f"INSERT INTO TRANSACTION VALUES('{maxtid()}','{b}','{Acno}','{dt.datetime.today()}','{'Withdraw'}','{blnc}')"
     
        cur.execute(qry)
        con.commit()   

    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return None
            else:
                if a==1:
                 deposit(Acno,b)
                elif a==3:
                  withdraw(Acno,b)
    finally:
            cur.close()
            con.close()
#==========================================================================================
def getMaxano():
    maxaid=''
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        qry="select max(AcNo) from ACCOUNT"
        cur.execute(qry) 
        row=cur.fetchone() #(None,)
        #print(row)    
        if row[0]==None:
            maxaid=1000
            
        else:
            maxaid=int(row[0])+1
        
               
    except pm.DatabaseError as e:
        con.rollback()
        print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
    return maxaid
#=============================================================================================
def new_pass():
    global admpass
    print('='*120)
    print(' '*gapvalue,*'NEW PASSWORD SETUP')
    print('='*120)
    print(' '*gapvalue,'ENTER PASSWORD TO VERIFY:',end='');    ps=input('').lower().strip()
    if ps==admpass:
     print(' '*gapvalue,'New Password:',end=' ');                            p=input('').lower().strip()
     admpass=p
     print(' '*gapvalue,'PASSWORD UPDATED SUCCESSFULLY')
     print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
     input()
    else:
        print(' '*gapvalue,'INCORRECT PASSWORD FOR VERIFICATION!...... PRESS ANY KEY TO CONTINUE!......')
        input()
#=============================================================================================
def getMaxCustid():
    maxid=''
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        qry="select max(custid) from Customer"
        cur.execute(qry) 
        row=cur.fetchone() #(None,)
        #print(row)    
        if row[0]==None:
            maxid=1
            
        else:
            maxid=int(row[0])+1
        
               
    except pm.DatabaseError as e:
        con.rollback()
        print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
    return maxid
#=================================================================================*
def deposit(Acno,a):
    print('='*120)
    title='CASH DEPOSITE'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
       #=============================================================================
        print(' '*gapvalue,'INPUT Cash To Be Deposited:',end=' ');               Balance=input('').lower().strip()
    
        qry=f"UPDATE ACCOUNT SET Balance=Balance+'{Balance}' WHERE AcNo='{Acno}' "
        
        cur.execute(qry)
        con.commit()
        print(' '*gapvalue,'BALANCE UPDATED SUCCESSFULLY')
        print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
        input()
        q=add_transaction(Acno,1,Balance,a)
        if q==None:
            return

    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!.....')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return
            else:
                deposit(Acno,a)
    finally:
            cur.close()
            con.close()
#=================================================================================
def withdraw(Acno,a):
    print('='*120)
    title='CASH WITHDRAW'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
       #=============================================================================
        print(' '*gapvalue,'INPUT Cash To WITHDRAWN:',end=' ');            Balance=input('').lower().strip()
    
        qry=f"""UPDATE ACCOUNT SET Balance=Balance-'{Balance}' WHERE AcNo='{Acno}'"""
        cur.execute(qry)
        con.commit()
        print(' '*gapvalue,'BALANCE UPDATED SUCCESSFULLY')
        add_transaction(Acno,2,Balance,a)
        print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
        input()

    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!.....')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return
            else:
                withdraw(Acno,a)
    finally:
            cur.close()
            con.close()
#===================================================================================
def user_trans(acno):
    print('='*120)
    title='DETAILS OF ALL TRANSACTIONS'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        t=pt.PrettyTable(['Tid','Custid','AcNo','Tdate','Ttype','Amount','Balance'])
        qry=f"select Tid,Custid,AcNo,Tdate,Ttype,Amount from TRANSACTION WHERE AcNo='{acno}'"
        cur.execute(qry)
        rows=cur.fetchall()
        #print(rows)
        if rows==():
            print(' '*gapvalue,'RECORD NOT FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
        else:
            for r in rows:
                t.add_row([r[0],r[1],r[2],r[3],r[4].UPPER(),r[5],r[6]])
            print(' '*gapvalue,t)
            print(' '*gapvalue,f'Total {len(rows)} records fetched. ')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
                
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!.....')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return
            else:
                user_trans(acno)
    finally:
            cur.close()
            con.close()  
#=================================================================================      
def add_Account():
    print('='*120)
    title='ACCOUNT DETAILS'
    print(' '*gapvalue,*title)
    print('='*120)
    try:
        
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor() # temporary 2D structure to store data.
        while(1):
            AcNo=getMaxano()
            Userid='ADMIN'
            print(' '*gapvalue,'User ID:',Userid,end=' ');                                
            print(' '*gapvalue,'Account Number:',AcNo);                         
            print(' '*gapvalue,'INPUT Customer ID:',end=' ');                          Custid=input('').lower().strip()
            print(' '*gapvalue,'INPUT Account Type[Saving/Current]:',end=' ');           AcType=input('').lower().strip()
            print(' '*gapvalue,'INPUT Balance:',end=' ');                                Balance=input('').lower().strip()
            print(' '*gapvalue,'INPUT Mobile Number:',end=' ');                          Mob=input('').lower().strip()
            print(' '*gapvalue,'INPUT Address:',end=' ');                                Address=input('').lower().strip()
            
            
            qry=f"INSERT INTO ACCOUNT VALUES({AcNo},'{Custid}','{Userid}',\
                '{AcType}','{Balance}','{Mob}','{Address}')"
            cur.execute(qry) 
            con.commit()
            print(' '*gapvalue,'ACCOUNT SAVED SUCCESSFULLY!')
            print(' '*gapvalue,'DO YOU WANT TO INSERT ONE MORE RECORD?',' '*gapvalue)
            print(' '*gapvalue,'PRESS [Y/N]:',end='')
            cce=input()
            if cce.lower().strip()!='y':
                break
        
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!...')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return
            else:
                add_Account()
    finally:
            cur.close()
            con.close()
#=================================================================================*
def add_Customer():
    print('='*120)
    title='CUSTOMER DETAILS'
    print(' '*gapvalue,*title)
    print('='*120)
    try:
        
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor() # temporary 2D structure to store data.
        while(1):
            custid=getMaxCustid()
            Userid='ADMIN'
            print(' '*gapvalue,'Userid:',Userid,end=''); 
            print(' '*gapvalue,'Customer ID:',custid)                                 
            print(' '*gapvalue,'INPUT First Name:',end=' ');                         Fname=input('').lower().strip()
            print(' '*gapvalue,'INPUT Last Name:',end=' ');                          Lname=input('').lower().strip()
            print(' '*gapvalue,'INPUT Aadhar:',end=' ');                             Aadhar=input('').lower().strip()
            print(' '*gapvalue,'INPUT Mobile Number:',end=' ');                      Mob=input('').lower().strip()
            print(' '*gapvalue,'INPUT Address:',end=' ');                            Address=input('').lower().strip()
            print(' '*gapvalue,'INPUT Gender[M/F]:',end=' ');                        Gender=input('').lower().strip()
            print(' '*gapvalue,'INPUT Date Of Birth[YYYY/MM/DD]:',end=' ');          dob=input('').lower().strip()

            
            qry=f"INSERT INTO CUSTOMER VALUES({custid},'{Userid}','{Fname}','{Lname}','{Aadhar}',\
                '{Mob}','{Address}','{Gender}','{dob}')"
            cur.execute(qry) 
            con.commit()
            print(' '*gapvalue,'CUSTOMER DETAILS SAVED SUCCESSFULLY')
            print(' '*gapvalue,'DO YOU WANT TO INSERT ONE MORE RECORD?',' '*gapvalue)
            print(' '*gapvalue,'PRESS [Y/N]:',end='')
            cce=input('')
            if cce.lower().strip()!='y':
                break
        
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!...')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return
            else:
               add_Customer()
    finally:
            cur.close()
            con.close()
#=================================================================================
def showall_transaction():
    print('='*120)
    title='DETAILS OF ALL TRANSACTIONS'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        t=pt.PrettyTable(['Tid','Custid','AcNo','Tdate','Ttype','Amount'])
        qry="select Tid,Custid,AcNo,Tdate,Ttype,Amount from TRANSACTION ORDER BY Tdate"
        cur.execute(qry)
        rows=cur.fetchall()
        #print(rows)
        if rows==():
            print(' '*gapvalue,'RECORD NOT FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
        else:
            for r in rows:
                t.add_row([r[0],r[1],r[2],r[3],r[4].upper(),r[5]])
            print(t)
            print(' '*gapvalue,f'Total {len(rows)} records fetched. ')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
                
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
#=================================================================================*
def showall_Account():
    print('='*120)
    title='DETAILS OF ALL ACCOUNTS'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        t=pt.PrettyTable(['AcNo','Custid','Userid','AcType','Balance','Mob','Address'])
        qry="select AcNo,Custid,userid,AcType,Balance,Mob,Address from ACCOUNT ORDER BY AcNo"
        cur.execute(qry)
        rows=cur.fetchall()
        #print(rows)
        if rows==():
            print(' '*gapvalue,'RECORD NOT FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
        else:
            for r in rows:
                t.add_row([r[0],r[1],r[2],r[3].upper(),r[4],r[5],r[6].upper()])
            print(t)
            print(' '*gapvalue,f'Total {len(rows)} records fetched. ')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
                
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
#=================================================================================*
def showall_customer():

    print('='*120)
    title='DETAILS OF ALL CUSTOMERS'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        t=pt.PrettyTable(['custid','Userid','Fname','Lname','Aadhar','Mob','Address','Gender','dob'])
        qry="select * from CUSTOMER"
        cur.execute(qry)
        rows=cur.fetchall()
        #print(rows)
        if rows==():
            print(' '*gapvalue,'RECORD NOT FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
        else:
            for r in rows:
                t.add_row([r[0],r[1],r[2].upper(),r[3].upper(),r[4],r[5],r[6].upper(),r[7].upper(),r[8]])
            print(t)
            print(' '*gapvalue,f'Total {len(rows)} records fetched. ')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
                
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
#=================================================================================
def update_customer(Custid):
    print('='*120)
    title='UPDATING CUSTOMER DETAILS'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        Userid='ADMIN'
       #=============================================================================
        print(' '*gapvalue,'USER ID:',Userid,end=' ');                                  
        print(' '*gapvalue,'CUSTOMER ID:',Custid)
        print(' '*gapvalue,'ENTER First Name:',end=' ');                         Fname=input('').lower().strip()
        print(' '*gapvalue,'ENTER Last Name:',end=' ');                          Lname=input('').lower().strip()
        print(' '*gapvalue,'ENTER Aadhar:',end=' ');                             Aadhar=input('').lower().strip()
        print(' '*gapvalue,'ENTER Mobile Number:',end=' ');                      Mob=input('').lower().strip()
        print(' '*gapvalue,'ENTER Address:',end=' ');                            Address=input('').lower().strip()
        print(' '*gapvalue,'ENTER Gender[M/F]:',end=' ');                        Gender=input('').lower().strip()
        print(' '*gapvalue,'ENTER Date Of Birth[YYYY/MM/DD]:',end=' ');                      dob=input('').lower().strip()

    
        qry=f"""UPDATE CUSTOMER SET  
        FName='{Fname}',LName='{Lname}',
        AAdhar='{Aadhar}',Mobile='{Mob}',
        ADDRESS='{Address}',Gender='{Gender}',DOB='{dob}'
        WHERE CustID='{Custid}' """
        #print(qry)
        cur.execute(qry)
        con.commit()
        print(' '*gapvalue,'RECORD UPDATED SUCCESSFULLY')
        print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
        input()

    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!...')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                return
            else:
                update_customer(Custid)
            
    finally:
            cur.close()
            con.close()
#=================================================================================*
def update_account(Acno):
    print('='*120)
    title='UPDATING ACCOUNT DETAILS'
    print(' '*40,*title)
    print('='*120)
    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
       #=============================================================================
        Userid='ADMIN'
        print(' '*gapvalue,'User ID:',end=' ');                                   
        print(' '*gapvalue,'Account Number:',Acno)                 
        print(' '*gapvalue,'INPUT Customer ID:',end=' ');                            Custid=input('').lower().strip()
        print(' '*gapvalue,'INPUT Account Type[Saving/Current]:',end=' ');           AcType=input('').lower().strip()
        print(' '*gapvalue,'INPUT Mobile Number:',end=' ');                          Mob=input('').lower().strip()
        print(' '*gapvalue,'INPUT Address:',end=' ');                                Address=input('').lower().strip()
 
    
        qry=f"""UPDATE ACCOUNT SET  AcNo='{Acno}',Userid='{Userid}',ACtype='{AcType}',\
        Mob='{Mob}',ADDRESS='{Address}'
        WHERE AcNo='{Acno}' """
        cur.execute(qry)
        con.commit()
        print(' '*gapvalue,'RECORD UPDATED SUCCESSFULLY')
        print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
        input()

    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
            print(' '*gapvalue,'TRY AGAIN!...')
            print(' '*gapvalue,'BACK TO MAIN MENU[Y/N]:',end='')
            y=input('')
            if y.lower().strip()in ['y','yes']:
                  return
            else:
               update_account(Acno)
    finally:
            cur.close()
            con.close()
#==================================================================================           
def find_by_accNo(u_accno):
    print('='*120)
    title='FINDING RECORD FROM ACCOUNT NUMBER'
    print(' '*40,*title)
    print('='*120)

    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        qry=f"select AcNo,CustID,UserID,ACtype,Balance,Mob,ADDRESS from ACCOUNT\
            WHERE  AcNo ='{u_accno}'"
        cur.execute(qry)
        rows=cur.fetchall()

        if rows==():
            print(' '*gapvalue,'RECORD NOT FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
            return False
        else:
            t=pt.PrettyTable(['AcNo','CustID','UserID','ACtype','Balance','Mobile','ADDRESS'])
            for r in rows:
                t.add_row([r[0],r[1],r[2],r[3].upper(),r[4],r[5],r[6].upper()])
            print(t)        
            print(' '*gapvalue,f'TOTAL {len(rows)} RECORD FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()    
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
#=================================================================================
def find_by_CUSID(CID):
    print('='*120)
    title='FINDING RECORD FROM CUSTOMER ID'
    print(' '*40,*title)
    print('='*120)

    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        qry=f"select CustID,UserID,FNAME,LNAME,AADHAR,MobILE,ADDRESS,GENDER,DOB from CUSTOMER\
            WHERE  CUSTID ='{CID}'"
        cur.execute(qry)
        rows=cur.fetchall()

        if rows==():
            print(' '*gapvalue,'RECORD NOT FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()
            return False
        else:
            t=pt.PrettyTable(['CustID','UserID','FNAME','LNAME','AADHAR','MOBILE','ADDRESS','GENDER','DOB'])
            for r in rows:
                t.add_row([r[0],r[1],r[2].upper(),r[3].upper(),r[4],r[5],r[6].upper(),r[7].upper(),r[8]])
            print(t)        
            print(' '*gapvalue,f'TOTAL {len(rows)} RECORD FOUND')
            print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
            input()    
    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()
#===================================================================================
def del_account(u_ano):
    print('='*120)
    title='DELETING ACCOUNT'
    print(' '*40,*title)
    print('='*120)

    try:
        con=pm.connect(user=usr,password=pwd,host='localhost',database=db)
        cur=con.cursor()
        #========================================
        
        qry=f'DELETE FROM ACCOUNT where AcNo={u_ano}'
        cur.execute(qry)
        con.commit()
        print(' '*gapvalue,'ACCOUNT DELETED SUCCESSFULLY')
        print(' '*gapvalue,'TYPE ENTER KEY TO CONTINUE....')
        input()

    except pm.DatabaseError as e:
        if con:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
    finally:
            cur.close()
            con.close()

#====================================================================================
#driver code

menu='''
                =======================================================================================================
                |                        B A N K    M A N A G E M E N T   S Y S T E M                             |
                -------------------------------------------------------------------------------------------------------
                | 1 | ADD CUSTOMER            | 6 | SHOW ALL CUSTOMERS              | 11 |    CASH DEPOSIT
                -------------------------------------------------------------------------------------------------------
                | 2 | ADD ACCOUNT             | 7 | SHOW ALL TRANSACTIONS           | 12 |  CASH WITHDRAW
                -------------------------------------------------------------------------------------------------------
                | 3 | EDIT CUSTOMER           | 8 | SEARCH ACCOUNT DETAILS          | 13 |  SEARCH TRANSACTION
                -------------------------------------------------------------------------------------------------------
                | 4 | EDIT ACCOUNT            | 9 | SEARCH CUSTOMER DETAILS        | 14 |  CHANGE PASSWORD
                -------------------------------------------------------------------------------------------------------
                | 5 | SHOW ALL ACCOUNTS      | 10 | DELETE ACCOUNT                  | 15 |  EXIT
                =======================================================================================================
                           
          '''  


print(' '*gapvalue,'INPUT PASSWORD:',end='')
pass_=input().lower().strip()
admpass='123'
if admpass!=pass_:
            print(' '*gapvalue,'PASSWORD INCORRECT ! ACCESS DENIED ! PRESS ANY KEY TO CONTINUE')
            input()
            #sys.exit()
else:
        while(1):
    
             print(menu)
             print(' '*gapvalue,'INPUT YOUR choice[1-15]: ',end='')
             c=input('').lower().strip()
             if c=='1':
                    add_Customer()
             elif c=='2':
                    add_Account()
             elif c=='3':
                    print(' '*gapvalue,'Enter Customer ID To Update:',end='')
                    Custid=input('').lower().strip()
                    if find_by_CUSID(Custid)==False:
                                 pass
                    else:
                
                       print(' '*gapvalue,'ARE YOU SURE TO UPDATE THE ABOVE RECORD?')
                       print(' '*gapvalue,'PRESS [Y/N] TO UPDATE THE RECORD=',end='')
                       ch_del=input().lower().strip()
                       if ch_del.lower().strip()!='y':
                             print(' '*gapvalue,'UPDATE ABORTED! PRESS ENTER KEY TO CONTINUE.....')
                             input()
                       else:
                             print(' '*gapvalue,'UPDATE INITIATED',end='')
                             time.sleep(1)
                             print('.',end='')
                             time.sleep(3)
                             print('.')
                             update_customer(Custid)
             elif c=='4':
                    print(' '*gapvalue,'Enter Account Number To Update:',end='')
                    Acno=input('').lower().strip()
                    if find_by_accNo(u_ano)==False:
                                 pass
                    else:
                
                       print(' '*gapvalue,'ARE YOU SURE TO UPDATE THE ABOVE RECORD?')
                       print(' '*gapvalue,'PRESS [Y/N] TO UPDATE THE RECORD=',end='')
                       ch_del=input().lower().strip()
                       if ch_del.lower().strip()!='y':
                             print(' '*gapvalue,'UPDATE ABORTED! PRESS ENTER KEY TO CONTINUE.....')
                             input()
                       else:
                             print(' '*gapvalue,'UPDATE INITIATED',end='')
                             time.sleep(1)
                             print('.',end='')
                             time.sleep(3)
                             print('.')
                             update_account(Acno)
             elif c=='5':
                    showall_Account()
             elif c=='6':
                    showall_customer()
             elif c=='7':
                    showall_transaction()
             elif c=='8':
                    print(' '*gapvalue,'Enter Account Number:',end='')
                    u_accno=input('').lower().strip()
                    find_by_accNo(u_accno)
             elif c=='9':
                print(' '*gapvalue,'Enter CUSTOMER ID:',end='')
                custid=input('').lower().strip()
                find_by_CUSID(custid)
             elif c=='10':
                    print(' '*gapvalue,'Enter Account Number To Be Deleted:',end='')
                    u_ano=input('').lower().strip()
                    if find_by_accNo(u_ano)==False:
                                 pass
                    else:
                
                       print(' '*gapvalue,'ARE YOU SURE TO DELETE THE RECORD?')
                       print(' '*gapvalue,'PRESS Y/y TO DELETE THE RECORD=',end='')
                       ch_del=input().lower().strip()
                       if ch_del.lower().strip()!='y':
                             print(' '*gapvalue,'DELETE ABORTED! PRESS ENTER KEY TO CONTINUE.....')
                             input()
                       else:
                             print(' '*gapvalue,'DELETE INITIATED',end='')
                             time.sleep(1)
                             print('.',end='')
                             time.sleep(3)
                             print('.')
                             del_account(u_ano)                  
             elif c=='11':
                print(' '*gapvalue,'Enter CUSTOMER ID:',end='')
                a=input().lower().strip()
                print(' '*gapvalue,'Enter Account Number:',end='')
                ac=input().lower().strip()
                if find_by_accNo(ac)==False:
                                 pass
                else:
                          deposit(ac,a)
             elif c=='12':
                print(' '*gapvalue,'Enter CUSTOMER ID:',end='')
                a=input().lower().strip()
                print(' '*gapvalue,'Enter Account Number:',end='')
                ac=input().lower().strip()
                if find_by_accNo(ac)==False:
                                 pass
                else:
                     withdraw(ac,a)
             elif c=='13':
                print(' '*gapvalue,'Enter CUSTOMER ID:',end='')
                a=input().lower().strip()
                print(' '*gapvalue,'Enter Account Number:',end='')
                accno=input().lower().strip()
                user_trans(accno,a)
             elif c=='14':
                new_pass()
                pass
             elif c=='15':
                print(' '*gapvalue,'THANK YOU FOR USING!......')
                print(' '*gapvalue,'PRESS ENTER KEY TO CONTINUE....')
                input()
                break
             else:
                    print(' '*gapvalue,'INVALID INPUT! Kindly use option [1-15]:')
                    print(' '*gapvalue,'PRESS ENTER KEY TO continue...')
                    input()
