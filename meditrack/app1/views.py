from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Login, Medicine, Customer, Sale
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import localdate, localtime
import json

def home(request):
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Login.objects.get(username=username, password=password)
            request.session['username'] = username
            return redirect('medicine_list')
        except Login.DoesNotExist:
            error = "Invalid username or password"
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_medicine(request):
    medicines = Medicine.objects.all()

    if request.method == 'POST':
        existing_medicine_id = request.POST.get('existing_medicine_id')
        new_medicine_name = request.POST.get('new_medicine_name', '').strip()
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        try:
            stock = int(stock)
        except (ValueError, TypeError):
            stock = None

        try:
            price = float(price)
        except (ValueError, TypeError):
            price = None

        if stock is None or price is None:
            error = "Please enter valid Stock and Price."
            return render(request, 'add_medicine.html', {'medicines': medicines, 'error': error})

        if existing_medicine_id:
            medicine = Medicine.objects.get(id=existing_medicine_id)
            medicine.stock = stock
            medicine.price = price
            medicine.save()
        elif new_medicine_name:
            medicine, created = Medicine.objects.get_or_create(
                name=new_medicine_name,
                defaults={
                    'stock': stock,
                    'price': price,
                }
            )
            if not created:
                medicine.stock = stock
                medicine.price = price
                medicine.save()
        else:
            error = "Please select an existing medicine or enter a new medicine name."
            return render(request, 'add_medicine.html', {'medicines': medicines, 'error': error})

        return redirect('/medicines')

    return render(request, 'add_medicine.html', {'medicines': medicines})

def medicine_list(request):
    query = request.GET.get('q')
    if query:
        medicines = Medicine.objects.filter(name__icontains=query)
    else:
        medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {
        'medicines': medicines,
        'query': query
    })

def add_sales(request):
    customers = Customer.objects.all()
    medicines = Medicine.objects.all()
    return render(request, 'sales.html', {'customers': customers, 'medicines': medicines})

def save_sale(request):
    if request.method == 'POST':
        existing_customer_id = request.POST.get('existing_customer')
        new_customer_name = request.POST.get('new_customer', '').strip()
        new_customer_phone = request.POST.get('new_customer_phone', '').strip()

        if new_customer_name:
            customer, created = Customer.objects.get_or_create(
                name=new_customer_name,
                phone=new_customer_phone
            )
        elif existing_customer_id:
            customer = Customer.objects.get(id=existing_customer_id)
        else:
            return JsonResponse({'error': 'Customer information required'}, status=400)

        sale_data_json = request.POST.get('sale_data')

        try:
            sale_data = json.loads(sale_data_json)
        except:
            return JsonResponse({'error': 'Invalid sale data'}, status=400)

        today = localdate()
        today_sales_count = Sale.objects.filter(created_at__date=today).count()
        invoice_number = today_sales_count + 1

        sale = Sale.objects.create(
            customer=customer,
            sale_data=sale_data,
            created_at=timezone.now(),
            invoice_number=invoice_number
        )

        for item in sale_data:
            med_id = item['medicine_id']
            qty = int(item['quantity'])
            medicine = Medicine.objects.get(id=med_id)
            if medicine.stock < qty:
                return JsonResponse({'error': f'Not enough stock for {medicine.name}'}, status=400)
            medicine.stock -= qty
            medicine.save()

        return redirect('sale_invoice', sale_id=sale.id)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def sale_invoice(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    customer = sale.customer
    sale_items = sale.sale_data

    all_sales = Sale.objects.all().order_by('created_at')

    sale_list = list(all_sales)
    try:
        invoice_number = sale_list.index(sale) + 1
    except ValueError:
        invoice_number = sale.id

    medicines = []
    grand_total = 0
    for item in sale_items:
        medicine = Medicine.objects.get(id=item['medicine_id'])
        quantity = item['quantity']
        total_price = medicine.price * quantity
        medicines.append({
            'name': medicine.name,
            'price': medicine.price,
            'quantity': quantity,
            'total': total_price
        })
        grand_total += total_price

    return render(request, 'sale_invoice.html', {
        'sale': sale,
        'customer': customer,
        'medicines': medicines,
        'grand_total': grand_total,
        'invoice_number': invoice_number,
    })

def view_sales(request):
    sales = Sale.objects.all().order_by('created_at')

    sales_data = []
    for idx, sale in enumerate(sales, start=1):
        grand_total = 0
        for item in sale.sale_data:
            medicine = Medicine.objects.get(id=item['medicine_id'])
            quantity = item['quantity']
            grand_total += medicine.price * quantity
        sales_data.append({
            'serial': idx,
            'id': sale.id,
            'customer_name': sale.customer.name,
            'created_at': localtime(sale.created_at),
            'grand_total': grand_total,
        })

    return render(request, 'view_sales.html', {'sales': sales_data})

def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    for item in sale.sale_data:
        med_id = item['medicine_id']
        qty = int(item['quantity'])
        medicine = Medicine.objects.get(id=med_id)
        medicine.stock += qty
        medicine.save()

    sale.delete()

    return redirect('view_sales')
