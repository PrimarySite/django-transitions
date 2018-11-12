Quickstart
-----------

Lets implement the following state machine.

 - The object starts of as 'under development' which can then be made 'live'.
 - From the 'live' state it can be marked as 'under maintenance'.
 - From all states the object can be marked as 'deleted'.
 - A 'deleted' object can be recovered into the 'under maintenance' state.
 - Whenever a transition occurs the datetime will be recorded in a datefield.

.. image:: lifcycle_state_diagram.svg

We start by defining the states and transitions

.. literalinclude:: ../../testapp/workflows.py
   :pyobject: LiveStatus

Next we create a mixin to create a state machine for the django model

.. literalinclude:: ../../testapp/workflows.py
   :pyobject: LifecycleStateMachineMixin

Set up the django model

.. literalinclude:: ../../testapp/models.py
   :pyobject: Lifecycle

Set up the django admin to include the workflow actions

.. literalinclude:: ../../testapp/admin.py
