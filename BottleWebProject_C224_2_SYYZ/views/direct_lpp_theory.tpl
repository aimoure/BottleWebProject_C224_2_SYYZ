% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
	<h1>Direct linear programming problem</h1>
	<p class="lead">
       The direct linear programming problem task is to maximize or minimize the linear function of a goal under conditions expressed by a system of linear constraints.
    </p>
</div>

<p class="intro-text">
	A primal linear programming problem (LPP) is an optimization task where you need to maximize or minimize a linear objective function Z = c<sub>1</sub>x<sub>1</sub> + c<sub>2</sub>x<sub>2</sub> + … + c<sub>n</sub>x<sub>n</sub>, subject to a system of linear constraints, for example, a<sub>1</sub>x<sub>3</sub> + a<sub>2</sub>x<sub>5</sub> ≤ b<sub>1</sub> and non-negativity conditions xi ≥ 0.
</p>
<p class="intro-text">
	The goal is to find such x<sub>i</sub> that Z is optimal.
</p>
<p class="intro-text">
	The main method for solving a primal LPP is the simplex method.
</p>
<p class="title-text">
	Simplex method
</p>
<p class="intro-text">
	The Simplex Method is an algorithm for solving LPP, which works as follows:
</p>
<p class="intro-text">
	1.	Convert the problem to standard form by adding slack variables for inequalities.
</p>
<p class="intro-text">
	2.	Construct the initial simplex table, where the rows are constraints, and the last row is the objective function.
</p>
<p class="intro-text">
	3.	Iteratively:
</p>
<p class="enumer-text">
	—	Check for optimality (are there negative coefficients in the Z-row?). 
</p>
<p class="enumer-text">
	—	If there are, select the pivot column (the largest negative number by modulus from the Z-row) and row (the minimum positive ratio of the right-hand side to the pivot column element), then update the table by introducing a new variable into the basis.
</p>
<p class="enumer-intro-text">
	All elements of the pivot row are divided by the pivot element, the elements of the pivot column are set to 0.
</p>
<p class="enumer-intro-text">
	The remaining elements are calculated using the formula:
</p>
<p class="enumer-intro-text" style='text-align: center'>
	a<sub>ij</sub>' = a<sub>ij</sub>  -  (a<sub>iq</sub> * a<sub>pj</sub>) / a<sub>pq</sub>, 
</p>
<p class="enumer-intro-text" style='text-align: center'>
	where p is the pivot row, q is the pivot column
</p>
<p class="enumer-text">
	—	Repeat until Z becomes optimal.
</p>
<p class="intro-text">
	4. Extract the solution: the values of xi and Z.
</p>