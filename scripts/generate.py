import csv,random,datetime,collections
from pathlib import Path
r=random.Random(3602026)
root=Path(__file__).resolve().parents[1]; out=root/'data';out.mkdir(exist_ok=True)
def save(name,cols,rows):
 with (out/f'{name}.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(cols);w.writerows(rows)
 print(name,len(rows))
 return len(rows)
counts={}
cities=['Toronto','Brampton','Mississauga','Vancouver','Calgary','Montreal','Ottawa','Edmonton','Winnipeg','Halifax']
provinces=['ON','ON','ON','BC','AB','QC','ON','AB','MB','NS']
customers=[]
for i in range(1,15001):
 j=r.randrange(len(cities)); signup=datetime.date(2023,1,1)+datetime.timedelta(days=r.randrange(1300))
 customers.append((i,f'Customer {i:05}',cities[j],provinces[j],signup.isoformat(),r.choice(['Organic','Paid Search','Referral','Social','Email'])))
counts['customers']=save('customers',['customer_id','customer_name','city','province','signup_date','acquisition_channel'],customers)
cat=['Electronics','Home & Kitchen','Fashion','Beauty','Sports','Books','Grocery','Office']
products=[]
for i in range(1,2501):
 c=cat[(i-1)%len(cat)]; price=r.randrange(800,120000,100)/100
 products.append((i,f'{c} Item {i:04}',c,f'{price:.2f}',r.choice(['Active','Active','Active','Discontinued'])))
counts['products']=save('products',['product_id','product_name','category','list_price','product_status'],products)
addresses=[]
for i in range(1,15001):
 j=r.randrange(len(cities)); k=j if r.random()<.8 else r.randrange(len(cities))
 addresses.extend([(2*i-1,i,'Billing',cities[j],provinces[j]),(2*i,i,'Shipping',cities[k],provinces[k])])
counts['customer_addresses']=save('customer_addresses',['address_id','customer_id','address_type','city','province'],addresses)
orders=[];items=[];payments=[];shipments=[];returns=[]
itemid=payid=shipid=returnid=0
start=datetime.date(2024,1,1);end=datetime.date(2026,9,30);days=(end-start).days
for oid in range(1,55001):
 cid=r.randrange(1,13001) # 2000 registered customers intentionally have no orders
 od=start+datetime.timedelta(days=r.randrange(days+1))
 status=r.choices(['Completed','Cancelled','Pending'],[.83,.09,.08])[0]
 n=r.choices([1,2,3,4],[.40,.34,.20,.06])[0];total=0
 chosen=r.sample(range(1,2301),n) # last 200 products never purchased
 for p in chosen:
  itemid+=1; qty=r.randint(1,3);unit=int(round(float(products[p-1][3])*100));total+=qty*unit
  items.append((itemid,oid,p,qty,f'{unit/100:.2f}'))
 expected=od+datetime.timedelta(days=r.randint(3,9))
 orders.append((oid,cid,od.isoformat(),expected.isoformat(),status,f'{total/100:.2f}',r.choice(['Web','Mobile'])))
 if status!='Cancelled' and r.random()>.065:
  if r.random()<.075: amount=total-r.randint(1,min(2500,total))
  elif r.random()<.025: amount=total+r.randint(100,2500)
  else:amount=total
  if r.random()<.19:
   first=amount//2
   for val in [first,amount-first]:
    payid+=1;payments.append((payid,oid,f'{val/100:.2f}',r.choice(['Card','Wallet','Bank Transfer']),od.isoformat(),'Captured'))
  else:
   payid+=1;payments.append((payid,oid,f'{amount/100:.2f}',r.choice(['Card','Wallet','Bank Transfer']),od.isoformat(),'Captured'))
 if status=='Completed' and r.random()<.96:
  shipid+=1; delay=r.randint(-2,5);ship_date=expected+datetime.timedelta(days=delay)
  shipment_status='Delivered' if r.random()<.91 else r.choice(['In Transit','Lost','Returned to Sender'])
  shipments.append((shipid,oid,ship_date.isoformat() if shipment_status=='Delivered' else '',shipment_status,r.choice(['Standard','Express'])))
  if shipment_status=='Delivered' and r.random()<.085:
   returnid+=1;item=r.choice(chosen);ret_date=ship_date+datetime.timedelta(days=r.randint(1,20))
   returns.append((returnid,oid,item,ret_date.isoformat(),r.choice(['Damaged','Wrong Item','Changed Mind','Defective']),r.choice(['Approved','Requested','Rejected'])))
# Keep main business facts referentially valid. Anomaly handling concerns absent related records, not broken FK.
for name,cols,rows in [
 ('orders',['order_id','customer_id','order_date','expected_delivery_date','order_status','order_amount','sales_channel'],orders),
 ('order_items',['order_item_id','order_id','product_id','quantity','unit_price'],items),
 ('payments',['payment_id','order_id','payment_amount','payment_method','payment_date','payment_status'],payments),
 ('shipments',['shipment_id','order_id','delivered_date','shipment_status','shipping_method'],shipments),
 ('returns',['return_id','order_id','product_id','return_date','return_reason','return_status'],returns)]:counts[name]=save(name,cols,rows)
assert len({o[0] for o in orders})==len(orders)
assert all(int(x[1])<=55000 for x in items+payments+shipments+returns)
assert all(int(x[2])<=2500 for x in items)
assert sum(int(round(float(x[4])*100))*int(x[3]) for x in items)==sum(int(round(float(x[5])*100)) for x in orders)
print('TOTAL',sum(counts.values()))
