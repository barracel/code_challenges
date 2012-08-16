import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;

public class RestaurantTables {
    static public class Table {
       // TODO(oscar): Make Table inmutable to force the recalculation of sizes
       Table(int size) {
           this.size = size;
           this.used = 0;
       }
       public int seats() {
           assert size >= used;
           return size - used;
       }
       private int size; //number of chairs around this table
       private int used; //number of chairs used
    }

    static public class CustomerGroup {
        CustomerGroup(int size) {
            this.size = size;
        }
        public final int size; //number of people in the group
    }

    static public class TableManager {
        /* Keeps a sorted list of sizes os tables ready to be used */
        Set<Integer> sizes;
        Map<Integer, List<Table>> tables;

        TableManager() {
            // Use Treeset to have a sorted set so the smallest sizes goes first
            sizes = new TreeSet<Integer>();
            tables = new HashMap<Integer, List<Table>>();
        }

        void add(Table table) {
            if (!tables.containsKey(table.seats())) {
                tables.put(table.seats(), new ArrayList<Table>());
            }
            tables.get(table.seats()).add(table);
            sizes.add(table.seats());
        }

        Table bookTable(int number_seats) {
            // Find the smallest table (We can replace the loop for a binary search)
            for (Integer size: sizes) {
                if (size >= number_seats) {
                    Table table = tables.get(size).remove(0);
                    if (tables.get(size).size() == 0) {
                        sizes.remove(size);
                    }
                    return table;
                }
            }
            return null;
        }

        void removeTable(Table table) {
            for (List<Table> t: tables.values()) {
                if (t.remove(table)) {
                    if (t.size() == 0) {
                        sizes.remove(table.seats());
                    }
                    return;
                }
            }
        }
    }

    static public class SeatingManager {
        TableManager tableManager;
        Map<CustomerGroup, Table> seated;
        List<CustomerGroup> waiting;

        /* Constructor */
        public SeatingManager(List<Table> tables) {
            tableManager = new TableManager();
            for (Table table : tables) {
                tableManager.add(table);
            }

            waiting = new ArrayList<CustomerGroup>();
            seated = new HashMap<Question2.CustomerGroup, Question2.Table>();
        }

        /* Group arrives and wants to be seated. */
        public void arrives(CustomerGroup group) {
            Table table = tableManager.bookTable(group.size);
            if (table != null) {
                table.used += group.size;
                seated.put(group, table);
                tableManager.add(table);
            } else {
                waiting.add(group);
            }
        }

        /* Whether seated or not, the group leaves the restaurant. */
        public void leaves(CustomerGroup group) {
            Table table = this.locate(group);
            if (table != null) {
                seated.remove(group);
                tableManager.removeTable(table);
                table.used -= group.size;
                // Find by waiting order if someone can use the table
                List<CustomerGroup> seated_groups = new ArrayList<Question2.CustomerGroup>();
                for (CustomerGroup g: waiting) {
                    if (table.seats() >= g.size) {
                        table.used += g.size;
                        seated.put(g, table);
                        seated_groups.add(g);
                    }
                }
                for (CustomerGroup g: seated_groups) {
                    waiting.remove(g);
                }
                // Remove and add table to force the computation of sizes
                tableManager.add(table);
            } else {
                waiting.remove(group);
            }
        }

        /* Return the table at which the group is seated, or null if
           they are not seated (whether they're waiting or already left). */
        public Table locate(CustomerGroup group) {
            if (seated.containsKey(group)) {
                return seated.get(group);
            } else {
                return null;
            }
        }
    }

    static void assertEquals(Set<Integer> set1, List<Integer> set2) {
        if (!set1.equals(new HashSet<Integer>(set2))) {
            throw new RuntimeException(set1 + " does not equals " + set2);
        }
    }

    static void assertNull(Object value) {
        if (value != null) {
            throw new RuntimeException(value + " is not null");
        }
    }

    static void assertNotNull(Object value) {
        if (value == null) {
            throw new RuntimeException(value + " is null");
        }
    }

    public static void main(String[] args) {
        Table T1_1 = new Table(1);
        Table T4_1 = new Table(4);
        Table T4_2 = new Table(4);
        Table T6_1 = new Table(6);

        CustomerGroup G1 = new CustomerGroup(1);
        CustomerGroup G2 = new CustomerGroup(2);
        CustomerGroup G2_2 = new CustomerGroup(1);
        CustomerGroup G3 = new CustomerGroup(3);
        CustomerGroup G4 = new CustomerGroup(4);
        CustomerGroup G5 = new CustomerGroup(5);
        CustomerGroup G6 = new CustomerGroup(6);

        List<Table> tables = Arrays.asList(T1_1, T4_2, T6_1, T4_1);
        SeatingManager manager = new SeatingManager(tables);


        assertEquals(manager.tableManager.sizes, Arrays.asList(1, 4, 6));
        manager.arrives(G3);
        manager.arrives(G2);
        manager.arrives(G4);
        manager.arrives(G1);
        assertNotNull(manager.locate(G3));
        assertNotNull(manager.locate(G2));
        assertNotNull(manager.locate(G4));
        assertNotNull(manager.locate(G1));
        assertEquals(manager.tableManager.sizes, Arrays.asList(0, 1, 2));


        manager.arrives(G6);
        assertNull(manager.locate(G6));

        manager.leaves(G2);
        assertNull(manager.locate(G2));
        assertNull(manager.locate(G6));
        assertEquals(manager.tableManager.sizes, Arrays.asList(0, 1, 2, 4));

        manager.arrives(G2);
        assertNull(manager.locate(G6));
        assertEquals(manager.tableManager.sizes, Arrays.asList(0, 1, 4));

        manager.leaves(G4);
        manager.leaves(G2);
        assertNull(manager.locate(G4));
        assertNotNull(manager.locate(G6));
        assertEquals(manager.tableManager.sizes, Arrays.asList(0, 1, 4));

        manager.leaves(G6);
        assertEquals(manager.tableManager.sizes, Arrays.asList(0, 1, 4, 6));

        manager.leaves(G1);
        manager.leaves(G3);
        assertEquals(manager.tableManager.sizes, Arrays.asList(1, 4, 6));

        System.out.println("ok");
    }
}