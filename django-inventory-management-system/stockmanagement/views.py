from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *

# View Homepage


def home(request):
    title = 'Welcome: This is the Home Page.'
    form = 'Welcome: This is the Home Page'
    context = {
        "title": title,
        "test": form,
    }
    return redirect('/list_items')


# view all items of the stock & search filter

@login_required
def list_items(request):
    header = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all().order_by("-pk")
    context = {

        "header": header,
        "queryset": queryset,
        "form": form

    }

    # search filter
    if request.method == 'POST':
        queryset = Stock.objects.filter(
            category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )

    # Export to CSV
    if form['export_to_CSV'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
        instance = queryset
        for stock in instance:
            writer.writerow([stock.category, stock.item_name, stock.quantity])
        return response

    context = {

        "header": header,
        "queryset": queryset,
        "form": form

    }
    return render(request, "list_items.html", context)


# add item in Stock & form validation

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/list_items')
    context = {

        "form": form,
        "title": "Add Item",

    }
    return render(request, "add_items.html", context)


# update product quantity

@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('/list_items')
    context = {

        'form': form

    }
    return render(request, 'add_items.html', context)


# delete product

'''@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully Deleted.')
        return redirect('/list_items')
    return render(request, "delete_items.html")'''


# item details

def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {

        "title": queryset.item_name,
        "queryset": queryset

    }
    return render(request, "stock_detail.html", context)


# process issue

@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        return redirect('/stock_detail/'+str(instance.id))

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }

    return render(request, "add_items.html", context)


# receive request

@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " +
                         str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")
        return redirect('/stock_detail/'+str(instance.id))

    context = {
        "title": 'Reaceive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


# updating the reorder level

@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " +
                         str(instance.item_name) + " is updated to " + str(instance.reorder_level))
        return redirect("/list_items")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)


# Order History

@login_required
def order_history(request):
    header = 'ORDER HISTORY'
    queryset = StockHistory.objects.all()
    form = OrderHistorySearchForm(request.POST or None)
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }

    # search with item name & date
    if request.method == 'POST':
        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value()
            ]
        )

        # CSV file export
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['ITEM NAME',
                 'ISSUE QUANTITY',
                 'ISSUE TO',
                 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [
                        stock.item_name,
                        stock.issue_quantity,
                        stock.issue_to,
                        stock.issue_price,
                        stock.phone_number,
                        stock.last_updated])
            return response
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "order_history.html", context)


''' SQL for stockmanagement_stockhistory table in MySql Database
DELIMITER //
DROP TRIGGER IF EXISTS after_stockmanagement_stock_update//
CREATE TRIGGER after_stockmanagemt_stock_update AFTER UPDATE ON stockmanagement_stock FOR EACH ROW
BEGIN
	IF new.issue_quantity = 0
		THEN INSERT INTO stockmanagement_stockhistory(
			id,
			last_updated,
			item_name,
			issue_quantity,
            issue_price,
			issue_by,
			quantity,
			receive_quantity,
			receive_by)
		VALUES(
			new.id,
			new.last_updated,
			new.item_name,
			new.issue_quantity,
            new.issue_price,
			new.issue_by,
			new.quantity,
			new.receive_quantity,
			new.receive_by);

	ELSEIF new.receive_quantity = 0
		THEN INSERT INTO stockmanagement_stockhistory(
			id,
			last_updated,
			item_name,
			receive_quantity,
			receive_by,
			issue_quantity,
            issue_price,
			issue_to,
			issue_by,
			quantity)
		VALUES(
			new.id,
			new.last_updated,
			new.item_name,
			new.receive_quantity,
			new.receive_by,
			new.issue_quantity,
            new.issue_price,
			new.issue_to,
			new.issue_by,
			new.quantity);
	END IF;
END//
DELIMITER ;'''

'''
ALTER TABLE `stockmanagement`.`stockmanagement_stockhistory`
CHANGE COLUMN `id` `id` INT(11) NULL,
DROP PRIMARY KEY;
'''