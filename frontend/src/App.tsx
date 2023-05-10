import React, {useEffect} from 'react';
import axios from 'axios';
import './App.css';

interface Processor {
    pk: number;
    name: string;
    cores: number;
    threads: number;
    frequency: number;
    boost_frequency: number;
    cache: number;
    lithography: number;
    tdp: number;
}

interface Response {
    time: number;
    rows: number;
    processors: Processor[];
}

interface FormValues {
    data: string;
    algorithm: string;
    aggrFunc: string;
    k: number;
}

interface Fields {
    cores: string;
    threads: string;
    frequency: string;
    boost_frequency: string;
    cache: string;
    lithography: string;
    tdp: string;
}

interface FieldProps {
    name: string;
    onChange: (string) => void;
    disabled: boolean;
}

function App() {
    const [response, setResponse] = React.useState<Response>();
    const [formValues, setFormValues] = React.useState<FormValues>({
        data: 'real',
        algorithm: 'naive',
        aggrFunc: 'max',
        k: 10
    });
    const [sortingFields, setSortingFields] = React.useState<Fields>({
        cores: '',
        threads: '',
        frequency: '',
        boost_frequency: '',
        cache: '',
        lithography: '',
        tdp: ''
    });
    const [loading, setLoading] = React.useState<boolean>(false);

    useEffect(() => {handleSubmit();}, [sortingFields]);

    const handleFormChange = (ev: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormValues({
            ...formValues,
            [ev.target.name]: ev.target.value
        });
    };

    const handleSubmit = async (ev?: React.FormEvent) => {
        ev?.preventDefault();

        let queryParams = '';
        for(const sortingField in sortingFields) {
            if(sortingFields[sortingField] !== '') {
                console.log(sortingFields[sortingField]);
                queryParams += `fields=${sortingFields[sortingField]}&`;
            }
        }
        queryParams += `data=${formValues.data}&`;
        queryParams += `algorithm=${formValues.algorithm}&`;
        queryParams += `aggr_func=${formValues.aggrFunc}&`;
        queryParams += `k=${formValues.k}`;
        setLoading(true);
        await axios.get('http://localhost:8000/processors/?' + queryParams).then(response => {
           setResponse({
               time: response.data.time,
               rows: response.data.rows_read,
               processors: response.data.data
           });
        });
        setLoading(false);
    };
    
    const handleFieldChange = (field: string, order: string) => {
        console.log(field + ' ' + order);
        setSortingFields({
            ...sortingFields,
            [field]: order === '' ? '' : field + '_' + order
        });
    };

    return (
        <div className='container'>
            <form onSubmit={handleSubmit}>
                    <label>
                        <input type="number" name="k" value={formValues.k} onChange={handleFormChange} disabled={loading}/>
                    </label>
                    <label>
                        <select name="data" value={formValues.data} onChange={handleFormChange} disabled={loading}>
                            <option value="real">Real</option>
                            <option value="experiment">Experiment</option>
                        </select>
                    </label>
                    <label>
                        <select name="algorithm" value={formValues.algorithm} onChange={handleFormChange} disabled={loading}>
                            <option value="naive">Naive</option>
                            <option value="treshold">Treshold</option>
                        </select>
                    </label>
                    <label>
                        <select name="aggrFunc" value={formValues.aggrFunc} onChange={handleFormChange} disabled={loading}>
                            <option value="max">Max</option>
                            <option value="min">Min</option>
                            <option value="sum">Sum</option>
                        </select>
                    </label>
                    <button type="submit" disabled={loading}>Submit</button>
                </form>
            <div>
                Time: {response?.time}
            </div>
            <div>
                Rows: {response?.rows}
            </div>
            <div className='table'>
                <div className='name'>
                    Name
                </div>
                <Field name='Cores' onChange={handleFieldChange.bind(this, 'cores')} disabled={loading} />
                <Field name='Threads' onChange={handleFieldChange.bind(this, 'threads')} disabled={loading} />
                <Field name='Frequency' onChange={handleFieldChange.bind(this, 'frequency')} disabled={loading} />
                <Field name='Boost frequency' onChange={handleFieldChange.bind(this, 'boost_frequency')} disabled={loading} />
                <Field name='Cache' onChange={handleFieldChange.bind(this, 'cache')} disabled={loading} />
                <Field name='Lithography' onChange={handleFieldChange.bind(this, 'lithography')} disabled={loading} />
                <Field name='TDP' onChange={handleFieldChange.bind(this, 'tdp')} disabled={loading} />
            {response?.processors.map(processor => (
                <React.Fragment key={processor.pk}>
                    <div className='name'>
                        {processor.name}
                    </div>
                    <div>
                        {processor.cores}
                    </div>
                    <div>
                        {processor.threads}
                    </div>
                    <div>
                        {processor.frequency + 'MHz'}
                    </div>
                    <div>
                        {processor.boost_frequency + 'MHz'}
                    </div>
                    <div>
                        {processor.cache + 'KB'}
                    </div>
                    <div>
                        {processor.lithography + 'nm'}
                    </div>
                    <div>
                        {processor.tdp + 'W'}
                    </div>
                </React.Fragment>
            ))}
            </div>
        </div>
    );
}

function Field(props: FieldProps) {
    const [order, setOrder] = React.useState('');

    useEffect(() => props.onChange(order), [order]);

    const handleClick = () => {
        switch (order) {
            case '':
                setOrder('desc');
                break;
            case 'desc':
                setOrder('asc');
                break;
            case 'asc':
                setOrder('');
                break;
        }
    };

    return (
        <div onClick={!props.disabled ? handleClick : () => {}} className={props.disabled ? 'field disabled' : 'field'}>
            {props.name} {order !== 'desc' && '\u25B4'} {order !== 'asc' && '\u25BE'}
        </div>
    );
}

export default App
