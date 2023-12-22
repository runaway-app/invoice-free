import pandas
import os
from os import path
from stat import S_IWRITE,S_IREAD
import csv
import sys
import datetime
import shutil

def repack(unpacked_str):
    
    send_str = ''
    count = 0
    for i in unpacked_str:
        if count < len(unpacked_str):
            send_str+=str(i)
            count+=1
            if count == len(unpacked_str):
                break
        send_str = send_str +'|'
        
    return send_str

#Code to get the base information from the user. This part is only to be run when the file is empty.

def get_base_info():
    print("Here you will have to input all the details about your company. (Write Exit for Exit)")
    company_name = input("Enter the name of your company: ")
    if company_name.lower() == 'exit':
        sys.exit("Thank you for choosing ProInvo. See you later!")
        return
    else:
        print("Company name is: ",company_name)
    gst_no = input("Enter the GST Number of your company (NA if not applicable): ")
    owner_name = input("Enter the name of your owner: ")
    contact_number = input("Enter the Contact Number of your company (NA if not applicable): ")
    email_ID = input("Enter the Email ID of your company (NA if not applicable): ")
    UPI_ID = input("Enter the UPI ID of your company for payments (NA if not applicable: ")
    invoice_prefix, series_start = invoice_series()
    my_id = hash(gst_no+owner_name)
    
    #-- Current Invoice number needs to be udpate to 001 everytime the prefix is changed --#
    #-- Potentially give an option to select 'start from' in future --#
    
    return company_name+'\n'+gst_no+'\n'+owner_name+'\n'+contact_number+'\n'+email_ID+'\n'+UPI_ID+'\n'+invoice_prefix+'\n'+series_start+'\n'+(str(my_id))

def invoice_series():
    
    invoice_prefix = input("Enter the Invoice Prefix you would like to use: ")
    
    while True:
        try:        
            series_length = int(input("How many digit long will the series be? : "))
            if series_length > 10 or series_length < 1 :
                print("Enter a number between 1 and 10")
                continue
            else:
                break
        except:
            print("Please enter a number between 1 and 10")
            continue
        break
    
    zeroes = ''
    
    for i in range(series_length)-1:
        zeroes+='0'
        
    series_start = zeroes+'1'
    
    return invoice_prefix, series_start

def update_inventory(item,variant_number,inventory_value):
    
    with open('product_records.csv','r') as p_file:
        with open('temp_file.csv','w') as temp:
            
            p_reader = csv.reader(p_file)
            t_f_writer = csv.writer(temp)
            
            for row in p_reader:
                if row[0] == item:
                    unpacked_inv = row[3].split('|')
                    unpacked_inv[variant_number]-=inventory_value
                    repacked_inv = repack(unpacked_inv)
                    row[3] = repacked_inv
                    t_f_writer.writerow(row)
                else:
                    t_f_writer.writerow(row)
    
    shutil.move('temp_file.csv','product_records,csv')
    
    return

def get_invoice_items():
    
    print("Enter the item, and then select the variant and then add quantity. Press enter without anyting to exit.")
    
    inv_items = []
    inv_price = []
    inv_quant = []
    
    while True:
        item = input("Enter name of your product: (type Done when finish): ")
        if item == '':
            return None, None, None, None
        elif item.lower() == 'done':
            break
        
        with open('product_records.csv','r') as prod_file:
            p_f_reader = csv.reader(prod_file)
            for rows in p_f_reader:
                if rows[0] == item or rows[4] == item:
                    variant_list = rows[1]
                    variant_cost_list = rows[2]
                    variant_inv = rows[3]
                    var_tax_rate = int(rows[5])
                    
                    var_dict = {}
                    print("Please select which variant you would like to choose?")
                    var_list_unpacked = variant_list.split('|')
                    var_cost_unpacked = variant_cost_list.split('|')
                    
                    var_cost_unpacked = [int(i) for i in var_cost_unpacked]
                       
                    var_inv_unpacked = variant_inv.split('|')
                    for i in range(len(var_list_unpacked)):
                        var_dict[i] = var_list_unpacked[i]
                    
                    for j in var_dict:
                        print(j," - ",var_dict[j])
                    
                    while True:    
                        try:
                            variant_input = int(input())
                            if variant_input > 0 and variant_input < len(var_list_unpacked):
                                break
                            else:
                                print("Please choose a valid option.")
                                continue
                        except:
                            print("Enter a number!")
                            continue
                        break
                    
                    inv_items.append(item+'-'+str(var_list_unpacked[variant_input]))
                    
                    while True:
                        try:
                            var_quantity = int(input("Enter the quantity of the product."))
                            if var_quantity > 0:
                                break
                            else:
                                print("Enter a postive number!")
                                continue
                        except:
                            print("Enter a number!")
                            continue
                        
                        break
                    
                    var_inv_unpacked[variant_input]-=var_quantity
                    update_inventory(item,variant_input,var_inv_unpacked[variant_input])
                    inv_quant.append(str(var_quantity))
                    inv_price.append((var_quantity*int(var_cost_unpacked[variant_input]))*(100+var_tax_rate)/100)
                    
                else:
                    cr_item = input("The item does not exist, or you dod not add it. Add item here. (Enter for exit)")
                    if cr_item == '':
                        continue
                    else:
                        coreFunctionality().enter_product()
                        continue
        break               
    
        
    invoice_value = 0
    
    for i in inv_price:
        invoice_value+=i
    
    return inv_items,inv_quant,inv_price,invoice_value
    
def get_cust_balance():
    while True:
        try:
            val = int(input("Enter Customer start balance: "))
            return val
        except:
            print("Enter a valid number.")
            continue
        

def invoice_number(*num):
    
    test = True
    
    with open('invoice_records.csv') as inv_file:
        reader = csv.reader(inv_file)
        
        for inv in reader:
            test = False
            pass
       
        if test:
            return get_header()+get_start()
    
    user_num = 0
    
    for n in num:
        user_num = n
        
    inv_unpacked = inv.split('-')
    
    for i,j in enumerate(inv_unpacked[1]):
        if j != '0':
            break
    
    if len(str(user_num)) > len(inv_unpacked[1]):
        print("Too large invoice number!")
        raise Exception()
    else:
        len_diff = len(inv_unpacked[1]) - len(str(user_num))
        str_temp = ''
        for _ in range(len_diff):
            str_temp += '0'
        
        return inv_unpacked[0] + str_temp + str(user_num)
    
    inv_str = ''
    for l in range(i,len(inv_unpacked[1])):
        inv_str+=(inv_unpacked[1][l])
    
    i_num = int(inv_str)+1
    
    return inv_unpacked[0]+str(i_num)

def get_header():
    
    with open('base_records.txt','r') as base_file:
        
        records = base_file.readlines()
        
        return records[6]

def get_start():
    
    with open('base_records.txt','r') as base_file:
        
        records = base_file.readlines()
        
        return records[7]
    

def add_payment(check, payment, cv):
    
    if check == 1:
        
        with open('invoice_records.csv','r') as i_file:
            with open('temp_file.csv','w') as temp:
                
                i_reader = csv.reader(i_file)
                t_f_writer = csv.writer(temp)
                
                for row in i_reader:
                    if row[1] == cv:                        
                        row[2] = row[2] + payment
                        t_f_writer.writerow(row)
                    else:
                        t_f_writer.writerow(row)
        
        shutil.move('temp_file.csv','product_records,csv')    
        return
        
    else:
        with open('customer_records.csv','r') as c_file:
            with open('temp_file.csv','w') as temp:
                
                c_reader = csv.reader(c_file)
                t_f_writer = csv.writer(temp)
                
                for row in c_reader:
                    if row[0] == cv:                        
                        row[6] = row[6] + payment
                        t_f_writer.writerow(row)
                    else:
                        t_f_writer.writerow(row)
        
        shutil.move('temp_file.csv','product_records,csv')    
        return

def make_invoice_num():
    pass

class coreFunctionality:
    
    @staticmethod
    def create_invoice(self):
        # -- Create an invoice using inputs by user -- #
        
        print("Enter the invoice details. To go back just press enter without typing.")
        customer_name = print("Enter the name of the customer: ")
        
        if customer_name == '':
            return
            #main_app() -- Contingency!
        
        with open('customer_records.csv','r') as cust_file_check:
            cust_reader = csv.reader(cust_file_check)
            
            for rows in cust_reader:
                if rows[0] == customer_name :
                    break
                else:
                    while True:    
                        choice_fwd = input("The customer doesn't exist. Do you wish to create a new customer? Y/N - ")
                        if choice_fwd.lower() == 'y':
                            self.create_customer()
                        elif choice_fwd.lower() == 'n':
                            print("You will be redirected to the create the invoice again.")
                            self.create_invoice()
                        else:
                            print("Enter a valid input.")
                            continue
                        
        while True:    
            
            invoice_date = input("Enter the Invoice date (Press Enter for Today): ")
            if invoice_date == '':
                invoice_date = str(datetime.date.today().day)+'/'+str(datetime.date.today().month)+'/'+str(datetime.date.today().year)
                break
            else:
                try:
                    check_date = invoice_date.split('/')
                    datetime.datetime(year=int(check_date[2]),month=int(check_date[1]),day=int(check_date[0]))
                    break
                except:
                    print("Enter a valid input.")
                    continue
            break
        
        # invoice_number = we will get it by adding 1 to the curr invoice in the base info file, which will be updated 
        # if regular numbering is kept, if changed, we do not update that.
        # Flirt with the idea of having a seperate file for inventory management.
        # Also an idea to have seperate lines for each variant.
        
        item_list,item_quantity,item_cost,invoice_value = get_invoice_items()
        
        if item_list == None or invoice_value == None:
            print("No item was added. Going back to the main menu.")
            return
        
        invoice_numb = invoice_number()
        
        while True:
            try:
                invoice_num = input("Invoice number is ",invoice_numb," if you want to change it, type the number else press enter.")
                if invoice_num == '':
                    break
                else:
                    with open('invoice_records','r') as file:
                        reader = csv.reader(file)
                        for rec in reader:
                            if rec[1] == invoice_number(int(invoice_num)) :
                                print("This invoice number exsits. Please enter again.")
                                continue
                            else:
                                invoice_numb = invoice_number(int(invoice_num))
                                break
            except:
                print("Enter a valid number.")
                continue
            
            break
        
        invoice_note = input("Enter any specific notes on this invocie: ")

        inv_row = customer_name+','+invoice_numb+','+str(invoice_value)+','+item_list+','+item_quantity+','+item_cost+','+str(invoice_date)+','+invoice_note
        inv_array = inv_row.split(',')
        
        os.chmod('invoice_records.csv',S_IWRITE)
        
        with open('invoice_records.csv','a') as inv_file:
            inv_writer = csv.writer(inv_file)
            inv_writer.writerow(inv_array)
        
        os.chmod('invoice_records.csv',S_IREAD)
        
        print("Invoice created successfully!")
        return 
    
    @staticmethod
    def create_customer(self):
        
        # --- Create a Customer using inpus by user --- #
        
        print("You have selected to create a customer. If you want to go back, press enter without typing anything.")
        customer_name = input("Enter Customer Name: ")
        if customer_name == '':
            return
        else:
            pass
        
        while True:
            try:
                customer_contact =  int(input("Enter Customer's Contact Info: "))
                if customer_contact > 4000000000 and customer_contact <= 9999999999 :
                    
                    with open('customer_records.csv','r') as cust_file_check:
                        cust_reader = csv.reader(cust_file_check)
                        
                        for rows in cust_reader:
                            if rows[1] == customer_contact:
                                print("This contact number exists, please enter correct number.")
                                continue
                            else:
                                break
                    
                else:
                    print("Please enter a valid 10 digit number.")
                    continue
            except:
                print("Please enter a valid 10 digit number.")
                pass    
            
            break
        
        
        customer_address = input("Enter Customer Address: ")
        customer_pin = input("Enter Customer Pin Code: ")
        customer_co_name = input("Enter Customer's Company Name: ")
        customer_tax_id = input("Enter Customer's Tax ID': ")
        customer_balance = get_cust_balance()
        customer_life_value = 0
        customer_note = input("Enter custom notes for this customer (leave blank if none): ")
    
        cust_row = customer_name+','+str(customer_contact)+','+customer_address+','+str(customer_pin)+','+customer_co_name+','+customer_tax_id+','+str(customer_balance)+','+str(customer_life_value)+','+customer_note
        cust_array = cust_row.split(',')
        
        os.chmod('customer_records.csv',S_IWRITE)
        
        with open('customer_records.csv','a') as cust_file:
            cust_writer = csv.writer(cust_file)
            cust_writer.writerow(cust_array)
        
        os.chmod('customer_records.csv',S_IREAD)
        
        print("Customer added successfully!")
        return
        
        #main_app() # -- Trying to return to the main function as a best-prectice.
    
    @staticmethod
    def enter_payment(self):
        
        # -- Payment Notes --#
        
        """ Once the payment details are put in, we ask them if they want to attach it
        to any invoice. We just ask an input. If the detail is an invoice, we check if
        the invoie exists and if it is a customer name, we give out a list of all the 
        invoice which are with that customer. And the patient can choose the invoice.
        And we will be able to attach the payment to the invoice."""
        
        print("Enter the customer or invoice for whom the payment will be added. Currency is INR.")
        cust_inv = input()
        
        if get_header() == cust_inv.split('-')[0]:
            
            with open('invoice_records.csv','r') as inv_rec:
                
                reader = csv.reader(inv_rec)
                
                for r in reader:
                    if r[1] == cust_inv:
                        while True:
                            try:
                                payment = int(input("Enter the payment recieved: "))
                                break
                            except:
                                print("Wrong input, please enter again.")
                                continue
                            break
                        
                        add_payment(1,payment,cust_inv)
                        
                        while True:
                            
                            try:
                                dec = input("Would you like to add this transaction in the file? (Y/N)")
                                if dec.lower() == 'y':
                                    #payment_id,customer_supplier,payment_amount,pay_to_pay,date_creation,due_date'
                                    print("Enter details as asked. Please note edits are only allowed once the record is complete.\n")
                                    payment_id = input("Enter the payment ID")
                                    c_s = input("Enter the customer or supplier name (will not be checked with the system).")
                                    pay_to_pay = input("Do you have to pay, or have you recieved this payment? (P/TP)")
                                    if pay_to_pay.lower() == 'p':
                                        p2p = 'pay'
                                    elif pay_to_pay.lower() == 'TP':
                                        p2p = 'topay'
                                    else:
                                        print("You will have to start again.")
                                        raise Exception()
                                        
                                    due_date = input("Enter the due date. DD-MM-YYYY.")
                                    date_form = '%d-%m-%Y'
                                    try:
                                       dateObject = datetime.datetime.strptime(due_date, date_form)
                                       print(dateObject)
                                    except ValueError:
                                       print("Incorrect data format, should be DD-MM-YYYY")
                                       continue
                                    date_today = str(datetime.date.today().day)+'/'+str(datetime.date.today().month)+'/'+str(datetime.date.today().year)
                                    
                                    with open('payment_records.csv','w') as p_file:
                                        
                                        writer = csv.writer(p_file)
                                        row = [payment_id,c_s,payment,p2p,date_today,due_date]
                                        writer.writerow(row)
                                        
                                        return
                                    
                                elif dec.lower() == 'n':
                                    return
                                else:
                                    raise Exception()
                            except:
                                print("Not a correct response, please try again.")
                                continue
                        
                        return
        else:
            
            with open('customer_records.csv','r') as cust_rec:
                
                reader = csv.reader(cust_rec)
                
                for r in reader:
                    if r[0] == cust_inv:
                        while True:
                            try:
                                payment = int(input("Enter the payment recieved: "))
                                break
                            except:
                                print("Wrong input, please enter again.")
                                continue
                            
                            break
                        
                        add_payment(2,payment,cust_inv)
                        
                        while True:
                            
                            try:
                                dec = input("Would you like to add this transaction in the file? (Y/N)")
                                if dec.lower() == 'y':
                                    #payment_id,customer_supplier,payment_amount,pay_to_pay,date_creation,due_date'
                                    print("Enter details as asked. Please note edits are only allowed once the record is complete.\n")
                                    payment_id = input("Enter the payment ID")
                                    pay_to_pay = input("Do you have to pay, or have you recieved this payment? (P/TP)")
                                    if pay_to_pay.lower() == 'p':
                                        p2p = 'pay'
                                    elif pay_to_pay.lower() == 'TP':
                                        p2p = 'topay'
                                    else:
                                        print("You will have to start again.")
                                        raise Exception()
                                        
                                    due_date = input("Enter the due date. DD-MM-YYYY.")
                                    date_form = '%d-%m-%Y'
                                    try:
                                       dateObject = datetime.datetime.strptime(due_date, date_form)
                                       print(dateObject)
                                    except ValueError:
                                       print("Incorrect data format, should be DD-MM-YYYY")
                                       continue
                                    date_today = str(datetime.date.today().day)+'/'+str(datetime.date.today().month)+'/'+str(datetime.date.today().year)
                                    
                                    with open('payment_records.csv','w') as p_file:
                                        
                                        writer = csv.writer(p_file)
                                        row = [payment_id,cust_inv,payment,p2p,date_today,due_date]
                                        writer.writerow(row)
                                        
                                        return
                                    
                                elif dec.lower() == 'n':
                                    return
                                else:
                                    raise Exception()
                            except:
                                print("Not a correct response, please try again.")
                                continue
                        
                        return
            
        
        print("The input did not belong to an Invoice or was a Customer, redirecting to the main menu.")
        return
    
    @staticmethod
    def enter_product(self):
        
        print("You have selected to create a product. If you want to go back, press enter without typing anything.")
        
        
        while True:
            try:
                product_name = input("Enter Product Name: ")
                if product_name == '':
                    return
                else:
                    with open('product_records.csv','r') as prod_file_check:
                        prod_reader = csv.reader(prod_file_check)
                        
                        for rows in prod_reader:
                            if rows[0] == product_name:
                                print("This product name exists, please enter a unique name.")
                                continue
            except:
                print("Please enter a valid product name.")
                pass  
        
        while True:
            try:
                product_variant_number = int(input("How many variants does this product has? (less than 100)"))
                break
            except:
                print("Enter a valid number less than 100.")
                continue
        
        product_variants = []
        product_variant_cost = []
        variant_inventory = []
    
        i = 0
        
        while True:
            while i < product_variant_number:
                i+=1
                curr_variant_name = input("Enter the name of variant no ", i+1," : ")
                try:
                    curr_variant_price = int(input("Enter the price of this variant: "))
                except:
                    print("Value is not a number.")
                    i-=1
                    continue
                
                if curr_variant_name == '':
                    print("Enter a valid variant name.")
                    i-=1
                    continue
                elif curr_variant_price <=0:
                    print("Enter a valid variant price.")
                    i-=1
                    continue
                else:
                    try:
                        curr_variant_inventory = int(input("Enter the inventory of the current product: "))
                        product_variants.append(curr_variant_name)
                        product_variant_cost.append(curr_variant_price)
                        variant_inventory.append(curr_variant_inventory)
                        break
                    except:
                        print("Enter a valid inventory number.")
                        i-=1
                        continue
            
            if i >= product_variant_number:
                break
        
        product_shorthand = input("Enter a shorthand for the product, if you want: ")
        product_tax_rate = input("Enter the tax rate for a product.")
        product_note = input("Enter any additional notes for your product.")
        
        #-- Code to upload an array in a CSV cell. Seperate by a '|' --#
        
        product_variant_list = ''
        var_ct = 0
        for i in product_variants:
            if var_ct < len(product_variants):
                product_variant_list = product_variant_list+i
                var_ct+=1
                if var_ct == len(product_variants):
                    break
                product_variant_list = product_variant_list+'|'
        
        product_var_cost_list = ''
        var_ct = 0
        for i in product_variant_cost:
            if var_ct < len(product_variant_cost):
                product_var_cost_list = product_var_cost_list+i
                var_ct+=1
                if var_ct == len(product_variant_cost):
                    break
                product_var_cost_list = product_var_cost_list+'|'
        
        product_var_inv_list = ''
        var_ct = 0
        for i in variant_inventory:
            if var_ct < len(variant_inventory):
                product_var_inv_list = product_var_inv_list+i
                var_ct+=1
                if var_ct == len(variant_inventory):
                    break
                product_var_inv_list = product_var_inv_list+'|'
        
        prod_row = product_name+','+product_variant_list+','+product_var_cost_list+','+product_var_inv_list+','+product_shorthand+','+product_tax_rate+','+product_note
        
        prod_array = prod_row.split(',')
        
        os.chmod('product_records.csv',S_IWRITE)
        
        with open('product_records.csv','a') as prod_file:
            prod_writer = csv.writer(prod_file)
            prod_writer.writerow(prod_array)
        
        os.chmod('product_records.csv',S_IREAD)
        
        print("Product added successfully!")
        
        return
    
    @staticmethod
    def edit_base_details(self):
        return
    
    @staticmethod
    def edit_invoice(self):
        return
    
    @staticmethod
    def delete_record(self):
        return
    
    @staticmethod
    def view_record(self):
        return

    @staticmethod
    def get_user_analytics(self):
        return
        
    @staticmethod    
    def exit_app():
        exit()

def main_app():    
    print("Hello, hope you are gaving a good day. How would you like to proceed?")
    print("0 - Exit\n1 - Create Invoice\n2 - Create Customer\n3 - Enter Payment\n4 - Create Product\n5 - Edit Base Details\n6 - Edit A Record\n7 - Delete A Record\n8 - View A Record\n9 - Get My Analytics")
    
    try:
        input_1 = int(input())
    except:
        print("Please enter only one digit as specified in the menu.")
        main_app()
    
    # --- Menu Functionality --- #
    
    function_list = ['exit_app','create_invoice','create_customer','enter_payment','enter_product','edit_base_details','edit_invoice','delete_record','view_record','get_user_analytics']
    
    functionRunner = coreFunctionality.__dict__.get(function_list[input_1])
    functionRunner.__func__()
    
    main_app()

if __name__ == "__main__":
    
    if path.exists("base_records.txt"):
        pass
    else:
        with open("base_records.txt",'w') as file:
            base_info = get_base_info()
            base_info_list = base_info.split(',')
            file.writelines(base_info_list)
            file_list = ['invoice_records.csv \n','payment_records.csv \n','product_records.csv \n'+'ustomer_records.csv \n']
        
            ivr = open("invoice_records.csv",'w')
            ptr = open("payment_records.csv",'w')
            pdr = open("product_records.csv",'w')
            ctr = open("customer_records.csv",'w')
            
            # -- Usage instruction text file shall be shared. -- #
            
            invoice_header = 'customer_name,invoice_number,invoice_value,item_list,item_quantity,item_cost,invoice_date,note'
            payment_header = 'payment_id,customer_supplier,payment_amount,pay_to_pay,date_creation,due_date'
            product_header = 'product_name,product_variants,product_variant_cost,variant_inventory,product_shorthand,product_tax_rate,note'
            customer_header = 'customer_name,customer_contact,customer_address,customer_pin,customer_co_name,customer_tax_id,customer_balance,customer_life_value,customer_note'
            
            # -- To add headers to these files. These files need to be prepped to recieve data as soon as they are created --#
            
            file.writelines(file_list)
        
            ivr.close()
            ptr.close()
            pdr.close()
            ctr.close()
            os.chmod('invoice_records.csv',S_IREAD)
            os.chmod('payment_records.csv',S_IREAD)
            os.chmod('product_records.csv',S_IREAD)
            os.chmod('customer_records.csv',S_IREAD)
            
            os.chmod("base_records.txt",S_IREAD)
            
    main_app()