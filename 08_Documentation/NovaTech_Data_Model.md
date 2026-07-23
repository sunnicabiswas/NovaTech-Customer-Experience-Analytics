# NovaTech Customer Experience Analytics — Data Model

```mermaid
flowchart LR

    %% Fact tables
    T["tbl_Support_Tickets<br/><br/>
    PK: Ticket_ID<br/>
    FK: Customer_ID<br/>
    FK: Product_ID<br/>
    FK: Agent_ID<br/>
    FK: Department_ID<br/>
    Issue_Category<br/>
    Priority_ID"]

    I["tbl_Interaction_History<br/><br/>
    PK: Interaction_ID<br/>
    FK: Customer_ID<br/>
    FK: Agent_ID"]

    S["tbl_Customer_Subscriptions<br/><br/>
    PK: Subscription_ID<br/>
    FK: Customer_ID<br/>
    FK: Product_ID"]

    %% Dimension tables
    C["tbl_Customers<br/><br/>
    PK: Customer_ID<br/>
    FK: Region_ID"]

    P["tbl_Products<br/><br/>
    PK: Product_ID"]

    A["tbl_Support_Agents<br/><br/>
    PK: Agent_ID"]

    D["tbl_Departments<br/><br/>
    PK: Department_ID"]

    R["tbl_Regions<br/><br/>
    PK: Region_ID"]

    IC["tbl_Issue_Categories<br/><br/>
    PK: Issue_Category"]

    PL["tbl_Priority_Levels<br/><br/>
    PK: Priority_ID"]

    SLA["tbl_SLA_Rules<br/><br/>
    Disconnected reference table"]

    %% Relationships
    C -->|"1 : many"| T
    P -->|"1 : many"| T
    A -->|"1 : many"| T
    D -->|"1 : many"| T
    IC -->|"1 : many"| T
    PL -->|"1 : many"| T

    R -->|"1 : many"| C

    C -->|"1 : many"| I
    A -->|"1 : many"| I

    C -->|"1 : many"| S
    P -->|"1 : many"| S

    SLA -.->|"Reference only"| T
```

## Model Notes

- `tbl_Support_Tickets` is the primary transactional fact table.
- `tbl_Interaction_History` captures customer-agent interactions.
- `tbl_Customer_Subscriptions` acts as a bridge between customers and products.
- Dimension tables provide filtering by customer, product, agent, department, region, issue category, and priority.
- `tbl_SLA_Rules` remains disconnected because the support-ticket dataset does not contain an `SLA_ID` key.
- Relationships use one-to-many cardinality with single-direction filtering.